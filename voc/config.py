"""Configurações centrais do projeto (lidas de variáveis de ambiente / .env)."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent

# Onde estão os CSVs do Kaggle e onde o índice vetorial será persistido
DATA_DIR = Path(os.getenv("DATA_DIR", ROOT / "data"))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", ROOT / "chroma_db"))
COLLECTION_NAME = "olist_reviews"

# Modelos (mesma família usada em aula: OpenAI + LangChain)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Parâmetros de recuperação
RETRIEVE_K = int(os.getenv("RETRIEVE_K", 40))        # candidatos buscados no índice
CONTEXT_K = int(os.getenv("CONTEXT_K", 12))          # avaliações enviadas ao LLM
MIN_RELEVANCE = float(os.getenv("MIN_RELEVANCE", 0.30))  # similaridade cosseno mínima
MIN_EVIDENCE = int(os.getenv("MIN_EVIDENCE", 5))     # nº mínimo de avaliações relevantes

# Pré-processamento
MIN_CHARS = int(os.getenv("MIN_CHARS", 15))          # descarta comentários muito curtos
MAX_CHARS = int(os.getenv("MAX_CHARS", 1000))        # trunca comentários gigantes
