"""Command for testing similarity search."""

import argparse

from services import build_vector_store, search_knowledge_base


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Question to search for in the PDF")
    parser.add_argument("-k", type=int, default=4, help="Number of results")
    args = parser.parse_args()

    _, vector_store = build_vector_store()
    results = search_knowledge_base(vector_store, args.query, k=args.k)
    for number, result in enumerate(results, start=1):
        print(
            f"\n[{number}] score={result.score:.4f} "
            f"source={result.source} page={result.page_number}\n"
            f"{result.content}"
        )


if __name__ == "__main__":
    main()
