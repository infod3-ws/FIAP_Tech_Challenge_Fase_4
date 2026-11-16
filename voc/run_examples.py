"""Roda perguntas de exemplo e grava docs/exemplos_perguntas_respostas.md.

Uso (após `python -m voc.build_kb`):
    python -m voc.run_examples
"""
from . import config
from .ask import render
from .rag import VoCRag
from .vectorstore import get_vectorstore

QUESTIONS = [
    # --- perguntas do enunciado ---
    "Quais são os principais problemas relatados pelos clientes em suas avaliações?",
    "O que os clientes relatam sobre problemas relacionados à entrega?",
    "Quais aspectos da experiência de compra são mais elogiados pelos clientes?",
    "Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos?",
    "Quais avaliações sustentam a conclusão de que existem problemas recorrentes de prazo de entrega?",
    # --- uso de metadados (nota) ---
    "Quais são os principais problemas nas avaliações com nota 1?",
    # --- guardrails: devem ser recusadas ---
    "Qual é a capital da França?",
    "Qual será o faturamento da empresa em 2027?",
    "O que os clientes dizem sobre o sabor das pizzas?",
]


def main() -> None:
    rag = VoCRag(get_vectorstore())
    out_path = config.ROOT / "docs" / "exemplos_perguntas_respostas.md"
    out_path.parent.mkdir(exist_ok=True)
    blocks = ["# Exemplos de perguntas e respostas\n",
              "Gerado automaticamente por `python -m voc.run_examples`.\n"]
    for q in QUESTIONS:
        print(f"-> {q}")
        blocks.append("```text\n" + render(rag.ask(q)) + "\n```\n")
    out_path.write_text("\n".join(blocks), encoding="utf-8")
    print(f"Salvo em {out_path}")


if __name__ == "__main__":
    main()
