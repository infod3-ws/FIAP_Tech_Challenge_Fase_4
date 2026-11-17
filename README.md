# Voice of Customer Intelligence com RAG (Olist)

Tech Challenge – Fase 4 (Deep Learning, NLP e IA Generativa) · POSTECH/FIAP

Solução RAG que permite a gestores e analistas fazerem perguntas em linguagem natural sobre as
**avaliações escritas de clientes** da base [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data)
e receberem respostas **fundamentadas em evidências rastreáveis** — ou uma recusa explícita quando
a base não sustenta a resposta.

## 1. Problema de negócio

Milhares de avaliações chegam todos os dias; a nota (1–5) mostra *quanto* o cliente está satisfeito,
mas o *porquê* está no texto. Ler tudo manualmente não escala. O sistema transforma os comentários
em uma base de conhecimento consultável: o gestor pergunta *"O que os clientes relatam sobre
problemas de entrega?"* e recebe uma síntese com as avaliações que a sustentam.

## 2. Arquitetura

```
Pergunta do gestor
      │
      ▼
[1] Processamento da pergunta (LLM, saída estruturada)
      • in_scope? • consulta reescrita "na voz do cliente" • filtro de nota (min/max)
      │ fora do escopo ──────────────────────────────────────► recusa
      ▼
[2] Embedding da consulta (text-embedding-3-small)
      ▼
[3] Busca semântica no ChromaDB (cosseno, top-40, filtro por nota)
      ▼
[4] Seleção: corte de relevância mínima + deduplicação + top-12
      │ < 5 avaliações relevantes ───────────────────────────► recusa
      ▼
[5] Contexto numerado: [R1] (nota | data | categoria) texto…
      ▼
[6] Geração (gpt-4o-mini, temperatura 0) — só com o contexto, citando [R#]
      │ modelo declara falta de evidência ───────────────────► recusa
      ▼
[7] Verificação de citações + resposta com evidências (✔ = citada)
```

Construção da base (offline, uma vez): `CSV → seleção/limpeza → Documents (texto + metadados) → embeddings → ChromaDB`.

## 3. Tecnologias

Python 3.10+ · LangChain (`langchain-core`, `langchain-openai`, `langchain-chroma`) · ChromaDB ·
OpenAI (`text-embedding-3-small`, `gpt-4o-mini`) · pandas · pydantic · pytest.

## 4. Estrutura do repositório

```
voc/
  config.py        parâmetros (modelos, limiares, caminhos)
  preprocess.py    seleção, limpeza e organização das avaliações em Documents
  vectorstore.py   ChromaDB + embeddings
  build_kb.py      CLI: constrói o índice
  rag.py           pipeline RAG + guardrails
  ask.py           CLI: perguntar (modo único ou interativo)
  run_examples.py  gera docs/exemplos_perguntas_respostas.md
tests/             testes offline (embeddings e LLM simulados)
docs/              exemplos de perguntas e respostas
```

## 5. Como instalar e executar

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env          # edite e coloque sua OPENAI_API_KEY
# baixe os CSVs do Kaggle e coloque em ./data (ver data/README.md)

python -m voc.build_kb        # 1) constrói a base (≈35–40 mil avaliações úteis; use --max-docs 5000 p/ testar)
python -m voc.ask "O que os clientes relatam sobre problemas de entrega?"   # 2) pergunta única
python -m voc.ask             # ou modo interativo
python -m voc.run_examples    # 3) (opcional) regenera docs/exemplos_perguntas_respostas.md
python -m pytest              # testes (não precisam de chave nem de dados)
```

**Reprodutibilidade:** dependências em `requirements.txt`; modelos e limiares configuráveis via `.env`;
amostragem com `random_state=42`; temperatura 0; `review_id` como id no índice (reexecutar não duplica).
Custo aproximado de indexar a base completa: poucos centavos de dólar.

## 6. Preparação da base (e justificativas)

Fonte: `olist_order_reviews_dataset.csv` (~100 mil avaliações).

| Etapa | Decisão | Por quê |
|---|---|---|
| Seleção | Mantém só avaliações com comentário (título e/ou mensagem) com ≥ 15 caracteres | mais da metade não tem texto e não há o que recuperar; textos como "ok" não carregam insight |
| Valores ausentes | Título ausente é ignorado; sem texto → descartada; data inválida → `desconhecida`; categoria ausente → `desconhecida` | Evita `None` no índice e não inventa dados |
| Limpeza | Normaliza espaços/quebras de linha, reduz alongamentos (`ótimooooo`→`ótimoo`), trunca em 1000 caracteres | Reduz ruído nos embeddings sem remover acentos/stopwords (o modelo de embedding usa o contexto) |
| Duplicatas | Remove `review_id` repetido e textos idênticos | Evita que "Muito bom" repetido 500× domine a recuperação e distorça a leitura de frequência |
| Organização | **1 avaliação = 1 documento**, sem chunking | Comentários são curtos (poucas frases): já são uma unidade semântica; quebrar perderia contexto |
| Embeddings | `text-embedding-3-small` | Multilíngue (funciona bem em português), barato e usado em aula |
| Indexação | ChromaDB persistente, distância de cosseno | Simples, local, suporta filtro por metadados |

## 7. Estratégia do pipeline RAG

- **Transformação da pergunta:** o gestor escreve em linguagem analítica ("principais padrões de
  reclamação"), o cliente escreve de forma coloquial ("meu produto nunca chegou"). Um LLM com
  saída estruturada (pydantic) reescreve a consulta *na voz do cliente*, define se a pergunta está no
  escopo e extrai filtros de nota.
- **Recuperação semântica:** busca top-40 por similaridade de cosseno, descarta abaixo de
  `MIN_RELEVANCE` (0,30), remove textos idênticos e envia ao LLM as 12 melhores.
- **Metadados (desafio adicional):** nota, mês da avaliação e categoria do produto (via join com
  itens/produtos) viajam com cada documento. A **nota é usada como filtro**: perguntas sobre
  "problemas/insatisfeitos" filtram nota ≤ 3; "elogios" filtram nota ≥ 4; "nota 1" filtra exatamente 1.
  Isso evita que elogios ou textos ambíguos poluam a resposta, aumentando a precisão da recuperação.
  Data e categoria aparecem no contexto, ajudando o modelo a contextualizar as evidências.
- **Contexto:** avaliações numeradas `[R1]…[R12]` com seus metadados.
- **Geração:** prompt que obriga a citar `[R#]`, proíbe conhecimento externo e **proíbe números
  exatos** (o modelo só vê uma amostra, não a base inteira).

## 8. Respostas fundamentadas e tratamento de falta de evidência

1. **Rastreabilidade:** cada afirmação cita `[R#]`; a saída lista as avaliações (nota, similaridade,
   data, categoria, `review_id`, texto) e marca com ✔ as efetivamente citadas. Se a resposta não
   citar nenhuma, um aviso é anexado.
2. **Três camadas de guardrail** contra respostas sem suporte:
   - *Escopo* — pergunta fora do domínio (ex.: "capital da França", "faturamento de 2027") é recusada
     antes da busca.
   - *Evidência insuficiente* — se menos de 5 avaliações passam do corte de relevância (ex.: "sabor
     das pizzas"), o sistema recusa **sem chamar o LLM de geração**.
   - *Recusa do modelo* — o prompt instrui a responder `NÃO HÁ EVIDÊNCIAS SUFICIENTES` quando o
     contexto não bastar.

## 9. Exemplos de perguntas e respostas

Veja [`docs/exemplos_perguntas_respostas.md`](docs/exemplos_perguntas_respostas.md)
(gerado por `python -m voc.run_examples`; inclui perguntas do enunciado, uso de filtro por nota e
casos de recusa).

## 10. Principais decisões, desafios e limitações

- **Top-k é uma amostra, não estatística.** O RAG responde "o que os clientes relatam", mas não
  "quantos %". Por isso o prompt veda números exatos. Quantificar exigiria agregação sobre a base
  inteira (ex.: classificação/clusterização de temas) — próximo passo natural.
- **Limiar de relevância é empírico.** 0,30 foi escolhido para `text-embedding-3-small`; se trocar de
  modelo, recalibre `MIN_RELEVANCE` com algumas perguntas dentro e fora do escopo.
- **Reescrita de consulta custa uma chamada a mais**, mas melhora a recuperação e viabiliza filtros e
  checagem de escopo na mesma etapa.
- **Dataset de 2016–2018:** os insights refletem esse período, não a operação atual.
- **Evolução:** busca híbrida (BM25 + vetorial), reranker, avaliação com conjunto de perguntas
  rotuladas, agregações por categoria/período e interface web.

## 11. Testes

`python -m pytest` valida limpeza dos dados, construção de filtros, guardrails (fora de escopo,
evidência insuficiente, recusa do modelo), citações e filtro de nota — com embeddings e LLM
simulados, sem rede.

## 12. Apresentação Executiva

[Assista à apresentação em vídeo da solução](https://github.com/infod3-ws/FIAP_Tech_Challenge_Fase_4/releases/download/v0.1-fiap-tc4-apresentacao/Apresentacao_Executiva_Tech_Challenge_Fase4.mp4)

O vídeo aborda o problema de negócio, a arquitetura RAG, a preparação da base de avaliações da Olist, a estratégia de recuperação com filtro por nota, uma demonstração ao vivo com as evidências recuperadas, o tratamento de perguntas sem evidência suficiente (Seção 8) e os principais desafios e decisões técnicas (Seção 10).
