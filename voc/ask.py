"""Interface de linha de comando.

Uso:
    python -m voc.ask "O que os clientes relatam sobre problemas de entrega?"
    python -m voc.ask            # modo interativo (digite 'sair' para encerrar)
"""
import sys

from .rag import Answer, VoCRag
from .vectorstore import get_vectorstore


def render(ans: Answer, max_evidences: int = 8) -> str:
    out = [f"\nPERGUNTA: {ans.question}"]
    if ans.plan:
        filtros = f"nota>={ans.plan.min_score}" if ans.plan.min_score else ""
        filtros += f" nota<={ans.plan.max_score}" if ans.plan.max_score else ""
        out.append(f"  consulta reescrita: {ans.plan.search_query}")
        out.append(f"  filtros: {filtros.strip() or 'nenhum'}")
    out.append(f"\nRESPOSTA:\n{ans.answer}")
    if ans.evidences:
        # citadas primeiro, depois as demais, mantendo a ordem de relevância
        ordered = sorted(ans.evidences, key=lambda e: not e.cited)[:max_evidences]
        out.append("\nEVIDÊNCIAS (✔ = citada na resposta):")
        for e in ordered:
            mark = "✔" if e.cited else " "
            out.append(
                f" {mark} [{e.ref}] nota {e.score} | sim={e.relevance} | {e.date} | "
                f"{e.category} | review_id={e.review_id[:8]}…\n       \"{e.text[:220]}\""
            )
    return "\n".join(out)


def main() -> None:
    rag = VoCRag(get_vectorstore())
    if len(sys.argv) > 1:
        print(render(rag.ask(" ".join(sys.argv[1:]))))
        return
    print("Voice of Customer RAG — digite sua pergunta (ou 'sair').")
    while True:
        q = input("\n> ").strip()
        if q.lower() in {"sair", "exit", "quit", ""}:
            break
        print(render(rag.ask(q)))


if __name__ == "__main__":
    main()
