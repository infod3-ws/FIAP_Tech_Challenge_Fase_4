"""Constrói a base de conhecimento: CSV -> documentos -> embeddings -> ChromaDB.

Uso:
    python -m voc.build_kb                 # base completa
    python -m voc.build_kb --max-docs 5000 # amostra rápida para testes
    python -m voc.build_kb --reset         # apaga o índice e recria
"""
import argparse
import shutil

from . import config
from .preprocess import load_reviews, to_documents
from .vectorstore import get_vectorstore

BATCH = 2000


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--max-docs", type=int, default=None, help="limita nº de avaliações (amostra)")
    ap.add_argument("--reset", action="store_true", help="apaga o índice existente antes de criar")
    args = ap.parse_args()

    if args.reset and config.CHROMA_DIR.exists():
        shutil.rmtree(config.CHROMA_DIR)

    docs = to_documents(load_reviews(max_docs=args.max_docs))
    store = get_vectorstore()

    for i in range(0, len(docs), BATCH):
        batch = docs[i : i + BATCH]
        # ids = review_id => rodar de novo não duplica registros
        store.add_documents(batch, ids=[d.metadata["review_id"] for d in batch])
        print(f"[index] {min(i + BATCH, len(docs))}/{len(docs)} documentos indexados")

    print(f"Pronto. Índice em: {config.CHROMA_DIR}")


if __name__ == "__main__":
    main()
