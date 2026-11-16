"""Seleção, limpeza e organização das avaliações da Olist em documentos.

Cada avaliação vira UM documento (não há chunking: os comentários são curtos,
~100 caracteres em média, então já são uma unidade semântica coesa).
"""
import re
from pathlib import Path
from typing import Optional

import pandas as pd
from langchain_core.documents import Document

from . import config

REVIEWS_CSV = "olist_order_reviews_dataset.csv"
ITEMS_CSV = "olist_order_items_dataset.csv"
PRODUCTS_CSV = "olist_products_dataset.csv"


def clean_text(text: str) -> str:
    """Normaliza espaços/quebras de linha e reduz alongamentos ('ótimooooo' -> 'ótimoo')."""
    text = re.sub(r"\s+", " ", str(text)).strip()
    text = re.sub(r"(.)\1{3,}", r"\1\1", text)
    return text


def build_text(title: Optional[str], message: Optional[str]) -> str:
    """Junta título (se existir) e comentário. Título ausente é simplesmente ignorado."""
    parts = [p for p in (title, message) if isinstance(p, str) and p.strip()]
    return clean_text(". ".join(p.strip().rstrip(".") for p in parts))


def _load_categories(data_dir: Path) -> Optional[pd.DataFrame]:
    """Categoria do produto por pedido (opcional: só se os CSVs existirem)."""
    items_p, prods_p = data_dir / ITEMS_CSV, data_dir / PRODUCTS_CSV
    if not (items_p.exists() and prods_p.exists()):
        return None
    items = pd.read_csv(items_p, usecols=["order_id", "product_id"])
    prods = pd.read_csv(prods_p, usecols=["product_id", "product_category_name"])
    cat = items.merge(prods, on="product_id", how="left")
    # Pedido com vários itens: usa a categoria mais frequente
    cat = (
        cat.dropna(subset=["product_category_name"])
        .groupby("order_id")["product_category_name"]
        .agg(lambda s: s.mode().iloc[0])
        .rename("category")
        .reset_index()
    )
    cat["category"] = cat["category"].str.replace("_", " ")
    return cat


def load_reviews(data_dir: Path = config.DATA_DIR, max_docs: Optional[int] = None) -> pd.DataFrame:
    """Lê e prepara as avaliações. Retorna um DataFrame limpo, 1 linha = 1 documento."""
    df = pd.read_csv(Path(data_dir) / REVIEWS_CSV)
    n_raw = len(df)

    # 1) Seleção: só interessa quem escreveu texto (sem texto não há o que recuperar)
    df["text"] = [
        build_text(t, m)
        for t, m in zip(df["review_comment_title"], df["review_comment_message"])
    ]
    df = df[df["text"].str.len() >= config.MIN_CHARS].copy()

    # 2) Limpeza: trunca textos gigantes e remove duplicatas (review_id e texto idêntico)
    df["text"] = df["text"].str.slice(0, config.MAX_CHARS)
    df = df.drop_duplicates(subset="review_id").drop_duplicates(subset="text")

    # 3) Valores ausentes / metadados
    df["review_score"] = df["review_score"].astype(int)
    df["date"] = pd.to_datetime(df["review_creation_date"], errors="coerce").dt.strftime("%Y-%m")
    df["date"] = df["date"].fillna("desconhecida")

    cats = _load_categories(Path(data_dir))
    if cats is not None:
        df = df.merge(cats, on="order_id", how="left")
    else:
        df["category"] = None
    df["category"] = df["category"].fillna("desconhecida")  # Chroma não aceita None

    df = df[["review_id", "order_id", "review_score", "date", "category", "text"]]
    df = df.reset_index(drop=True)
    if max_docs:
        df = df.sample(n=min(max_docs, len(df)), random_state=42).reset_index(drop=True)

    print(f"[preprocess] {n_raw} avaliações brutas -> {len(df)} documentos úteis")
    return df


def to_documents(df: pd.DataFrame) -> list[Document]:
    """Converte o DataFrame em Documents do LangChain (texto + metadados)."""
    return [
        Document(
            page_content=row.text,
            metadata={
                "review_id": row.review_id,
                "order_id": row.order_id,
                "score": int(row.review_score),
                "date": row.date,
                "category": row.category,
            },
        )
        for row in df.itertuples(index=False)
    ]
