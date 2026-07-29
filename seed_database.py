"""Command: PDF -> Documents -> chunks -> Qdrant."""

from services import seed_knowledge_base


def main() -> None:
    report = seed_knowledge_base()
    print(
        f"{report.status}: {report.pages} PDF pages -> {report.chunks} chunks "
        f"in collection '{report.collection}'"
    )


if __name__ == "__main__":
    main()
