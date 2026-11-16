import pandas as pd

from voc.preprocess import build_text, clean_text, load_reviews, to_documents


def _write_csvs(tmp_path):
    pd.DataFrame({
        "review_id": ["a", "b", "c", "d", "a", "e"],
        "order_id": ["o1", "o2", "o3", "o4", "o1", "o5"],
        "review_score": [1, 5, 3, 4, 1, 2],
        "review_comment_title": ["Atraso", None, None, None, "Atraso", None],
        "review_comment_message": [
            "O produto demorou muito para chegar",   # ok
            "ótimooooo produto, chegou antes!",      # alongamento
            None,                                    # sem comentário -> removido
            "ok",                                    # curto -> removido
            "O produto demorou muito para chegar",   # review_id duplicado
            "Entrega ruim,\r\nnunca chegou o pedido",  # quebra de linha
        ],
        "review_creation_date": ["2018-03-01"] * 6,
        "review_answer_timestamp": ["2018-03-02"] * 6,
    }).to_csv(tmp_path / "olist_order_reviews_dataset.csv", index=False)


def test_clean_text():
    assert clean_text("ótimooooo   bom\r\n") == "ótimoo bom"


def test_build_text_ignora_titulo_ausente():
    assert build_text(None, "Chegou rápido") == "Chegou rápido"
    assert build_text("Ruim", "Não gostei") == "Ruim. Não gostei"


def test_load_reviews_filtra_limpa_e_deduplica(tmp_path):
    _write_csvs(tmp_path)
    df = load_reviews(tmp_path)
    assert set(df["review_id"]) == {"a", "b", "e"}
    assert (df["category"] == "desconhecida").all()      # sem CSV de produtos
    assert "\n" not in " ".join(df["text"])
    docs = to_documents(df)
    assert docs[0].metadata["score"] in {1, 2, 5}
    assert all(isinstance(d.metadata["category"], str) for d in docs)
