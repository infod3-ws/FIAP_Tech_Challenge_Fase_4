"""Criação/abertura do índice vetorial (ChromaDB, distância de cosseno)."""
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from . import config


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=config.EMBEDDING_MODEL)


def get_vectorstore(embeddings=None, persist_directory=None) -> Chroma:
    """Abre (ou cria) a coleção. `hnsw:space=cosine` faz o score virar 1 - distância."""
    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=embeddings or get_embeddings(),
        persist_directory=str(persist_directory or config.CHROMA_DIR),
        collection_metadata={"hnsw:space": "cosine"},
    )
