"""Pipeline RAG de Voice of Customer.

Fluxo:
  pergunta -> (1) reescrita + filtros + checagem de escopo (LLM)
           -> (2) busca semântica no ChromaDB (com filtro por nota)
           -> (3) filtro de relevância mínima + deduplicação
           -> (4) guardrail de evidência suficiente
           -> (5) montagem do contexto numerado [R1], [R2]...
           -> (6) geração fundamentada com citações
           -> (7) verificação das citações e retorno das evidências
"""
import re
from dataclasses import dataclass, field
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from . import config

NO_EVIDENCE = "NÃO HÁ EVIDÊNCIAS SUFICIENTES"

# --------------------------------------------------------------------------- #
# 1) Processamento da pergunta
# --------------------------------------------------------------------------- #
REWRITE_SYSTEM = """Você prepara consultas para uma busca semântica em avaliações de \
clientes de um e-commerce brasileiro (Olist, 2016-2018). Analise a pergunta de um gestor e devolva:

- in_scope: true se a pergunta pode ser respondida com avaliações/comentários de clientes \
(problemas, elogios, padrões, insatisfação, entrega, qualidade, atendimento, produtos...). \
Perguntas sobre clientes satisfeitos ou insatisfeitos, reclamações ou padrões nas avaliações são SEMPRE true. \
false somente para assuntos sem relação com avaliações (conhecimento geral, previsões, faturamento, preços...). \
Na dúvida, use true.
- search_query: reescreva o tema em português, como um CLIENTE escreveria a avaliação, com \
termos concretos e sinônimos. Remova palavras analíticas como "principais", "padrões", "mais \
frequentes". Ex.: "problemas de entrega" -> "produto não chegou, entrega atrasou, demorou \
muito para receber o pedido".
- min_score / max_score (1 a 5, ou null): use SOMENTE se a pergunta falar de satisfação ou nota. \
min_score é a nota MÍNIMA; max_score é a nota MÁXIMA. \
Perguntas sobre problemas, reclamações, defeitos, insatisfação, queixas ou nota baixa -> max_score=3 (NUNCA use min_score). \
Elogios, satisfação, nota alta -> min_score=4 (NUNCA use max_score). \
Nota explícita (ex.: "nota 1") -> min_score e max_score iguais. \
Caso contrário, ambos null."""


class QueryPlan(BaseModel):
    in_scope: bool = Field(description="A pergunta pode ser respondida com avaliações de clientes?")
    search_query: str = Field(description="Consulta de busca semântica reescrita em português")
    min_score: Optional[int] = Field(default=None, ge=1, le=5)
    max_score: Optional[int] = Field(default=None, ge=1, le=5)


def build_filter(plan: QueryPlan) -> Optional[dict]:
    """Traduz os filtros de nota do plano para a sintaxe de filtro do Chroma."""
    conds = []
    if plan.min_score:
        conds.append({"score": {"$gte": plan.min_score}})
    if plan.max_score:
        conds.append({"score": {"$lte": plan.max_score}})
    if not conds:
        return None
    return conds[0] if len(conds) == 1 else {"$and": conds}


# --------------------------------------------------------------------------- #
# 5/6) Geração fundamentada
# --------------------------------------------------------------------------- #
ANSWER_SYSTEM = f"""Você é um analista de Voz do Cliente. Responda à pergunta do gestor \
usando EXCLUSIVAMENTE as avaliações numeradas fornecidas no contexto.

Regras:
1. Toda afirmação deve citar as avaliações que a sustentam, no formato [R1] ou [R2][R5].
2. Não use conhecimento externo e não invente fatos. Você vê apenas uma AMOSTRA das avaliações \
mais relevantes, não a base inteira: NÃO informe percentuais, contagens totais ou rankings \
exatos. Use linguagem qualitativa ("aparece em várias das avaliações analisadas").
3. Só responda "NÃO HÁ EVIDÊNCIAS SUFICIENTES" se NENHUMA avaliação tratar do tema perguntado. \
Se houver avaliações relevantes, resuma os temas que aparecem nelas, mesmo que sejam variados. \
Se não houver nenhuma, responda começando exatamente com "{NO_EVIDENCE}" e explique em uma frase.
4. Responda em português, de forma objetiva: no máximo 6 tópicos curtos."""


@dataclass
class Evidence:
    ref: str            # "R1", "R2"...
    review_id: str
    score: int
    relevance: float    # similaridade cosseno (0-1)
    date: str
    category: str
    text: str
    cited: bool = False


@dataclass
class Answer:
    question: str
    plan: Optional[QueryPlan]
    answer: str
    grounded: bool                      # False = sistema se recusou a responder
    reason: str = ""                    # por que a recusa aconteceu (se aplicável)
    evidences: list[Evidence] = field(default_factory=list)


def format_context(evidences: list[Evidence]) -> str:
    lines = []
    for e in evidences:
        meta = f"nota {e.score}/5 | {e.date} | categoria: {e.category}"
        lines.append(f"[{e.ref}] ({meta}) {e.text}")
    return "\n".join(lines)


class VoCRag:
    def __init__(self, vectorstore, llm=None):
        self.vs = vectorstore
        self.llm = llm or ChatOpenAI(model=config.LLM_MODEL, temperature=0, timeout=60, max_retries=3)

    # (1) -------------------------------------------------------------- #
    def plan_query(self, question: str) -> QueryPlan:
        planner = self.llm.with_structured_output(QueryPlan)
        return planner.invoke([SystemMessage(content=REWRITE_SYSTEM), HumanMessage(content=question)])

    # (2)(3) ----------------------------------------------------------- #
    def retrieve(self, plan: QueryPlan, min_relevance: float = None, k: int = None) -> list[Evidence]:
        min_relevance = config.MIN_RELEVANCE if min_relevance is None else min_relevance
        k = k or config.RETRIEVE_K
        hits = self.vs.similarity_search_with_relevance_scores(
            plan.search_query, k=k, filter=build_filter(plan)
        )
        seen, evidences = set(), []
        for doc, rel in hits:  # já vêm ordenados do mais para o menos similar
            if rel < min_relevance:
                continue
            key = doc.page_content.lower()
            if key in seen:  # evita contar a mesma frase repetida várias vezes
                continue
            seen.add(key)
            m = doc.metadata
            evidences.append(
                Evidence(
                    ref=f"R{len(evidences) + 1}",
                    review_id=m.get("review_id", ""),
                    score=int(m.get("score", 0)),
                    relevance=round(float(rel), 3),
                    date=m.get("date", ""),
                    category=m.get("category", ""),
                    text=doc.page_content,
                )
            )
        return evidences

    # pipeline completo ------------------------------------------------ #
    def ask(self, question: str) -> Answer:
        plan = self.plan_query(question)

        # Guardrail 1: pergunta fora do escopo da base
        if not plan.in_scope:
            return Answer(
                question, plan,
                f"{NO_EVIDENCE}: a pergunta está fora do escopo da base (avaliações de clientes).",
                grounded=False, reason="fora_do_escopo",
            )

        evidences = self.retrieve(plan)

        # Guardrail 2: poucas avaliações realmente relevantes
        if len(evidences) < config.MIN_EVIDENCE:
            return Answer(
                question, plan,
                f"{NO_EVIDENCE}: encontrei apenas {len(evidences)} avaliação(ões) relevante(s) "
                f"(mínimo exigido: {config.MIN_EVIDENCE}).",
                grounded=False, reason="evidencia_insuficiente", evidences=evidences,
            )

        evidences = evidences[: config.CONTEXT_K]
        user_msg = (
            f"Pergunta do gestor: {question}\n\n"
            f"Avaliações recuperadas:\n{format_context(evidences)}"
        )
        text = self.llm.invoke(
            [SystemMessage(content=ANSWER_SYSTEM), HumanMessage(content=user_msg)]
        ).content.strip()

        # Guardrail 3: o próprio LLM pode recusar (regra 3 do prompt)
        if text.upper().startswith(NO_EVIDENCE):
            return Answer(question, plan, text, grounded=False,
                          reason="recusa_do_modelo", evidences=evidences)

        # Rastreabilidade: marca quais evidências foram realmente citadas
        cited = set(re.findall(r"\[R(\d+)\]", text))
        for e in evidences:
            e.cited = e.ref[1:] in cited
        if not any(e.cited for e in evidences):
            text += "\n\n(Atenção: a resposta não citou nenhuma avaliação; trate com cautela.)"

        return Answer(question, plan, text, grounded=True, evidences=evidences)
