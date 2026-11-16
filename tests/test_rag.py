"""Testa o pipeline com embeddings determinísticos e um LLM de mentira (sem rede)."""
import pytest
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.messages import AIMessage

from voc import config, rag
from voc.rag import NO_EVIDENCE, QueryPlan, VoCRag, build_filter


class StubLLM:
    def __init__(self, plan, answer="- Atrasos na entrega [R1][R2]."):
        self.plan, self.answer = plan, answer

    def with_structured_output(self, schema):
        plan = self.plan

        class _P:
            def invoke(self, _msgs):
                return plan

        return _P()

    def invoke(self, _msgs):
        return AIMessage(content=self.answer)


@pytest.fixture()
def store():
    vs = Chroma(
        collection_name="teste_voc", embedding_function=DeterministicFakeEmbedding(size=32),
        collection_metadata={"hnsw:space": "cosine"},
    )
    docs = [
        Document(page_content=f"entrega atrasou muito, comentário {i}",
                 metadata={"review_id": f"r{i}", "score": 1 + i % 5, "date": "2018-01",
                           "category": "x"})
        for i in range(20)
    ]
    vs.add_documents(docs, ids=[d.metadata["review_id"] for d in docs])
    return vs


def test_build_filter():
    assert build_filter(QueryPlan(in_scope=True, search_query="x")) is None
    assert build_filter(QueryPlan(in_scope=True, search_query="x", max_score=3)) == {"score": {"$lte": 3}}
    f = build_filter(QueryPlan(in_scope=True, search_query="x", min_score=1, max_score=1))
    assert f == {"$and": [{"score": {"$gte": 1}}, {"score": {"$lte": 1}}]}


def test_fora_do_escopo_nao_chama_retrieval(store):
    r = VoCRag(store, StubLLM(QueryPlan(in_scope=False, search_query="")))
    ans = r.ask("Qual a capital da França?")
    assert not ans.grounded and ans.reason == "fora_do_escopo" and NO_EVIDENCE in ans.answer


def test_evidencia_insuficiente(store, monkeypatch):
    monkeypatch.setattr(config, "MIN_RELEVANCE", 0.99)  # nada passa do corte
    r = VoCRag(store, StubLLM(QueryPlan(in_scope=True, search_query="entrega")))
    ans = r.ask("entrega?")
    assert not ans.grounded and ans.reason == "evidencia_insuficiente"


def test_resposta_fundamentada_com_citacoes(store, monkeypatch):
    monkeypatch.setattr(config, "MIN_RELEVANCE", -1.0)  # tudo passa
    r = VoCRag(store, StubLLM(QueryPlan(in_scope=True, search_query="entrega atrasou")))
    ans = r.ask("problemas de entrega?")
    assert ans.grounded and len(ans.evidences) == config.CONTEXT_K
    assert [e.cited for e in ans.evidences[:3]] == [True, True, False]


def test_filtro_de_nota_e_aplicado(store, monkeypatch):
    monkeypatch.setattr(config, "MIN_RELEVANCE", -1.0)
    plan = QueryPlan(in_scope=True, search_query="entrega", max_score=2)
    ev = VoCRag(store, StubLLM(plan)).retrieve(plan, min_relevance=-1.0)
    assert ev and all(e.score <= 2 for e in ev)


def test_recusa_do_modelo_vira_nao_fundamentada(store, monkeypatch):
    monkeypatch.setattr(config, "MIN_RELEVANCE", -1.0)
    llm = StubLLM(QueryPlan(in_scope=True, search_query="pizza"), answer=f"{NO_EVIDENCE}: nada sobre pizza.")
    ans = VoCRag(store, llm).ask("pizza?")
    assert not ans.grounded and ans.reason == "recusa_do_modelo"
