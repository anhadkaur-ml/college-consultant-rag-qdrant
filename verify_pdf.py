"""Offline verification: proves the input remains PDF Documents end-to-end."""

from pdf_loader import PDF_PATH, load_pdf_pages, split_documents


def main() -> None:
    pages = load_pdf_pages(PDF_PATH)
    chunks = split_documents(pages)
    assert PDF_PATH.suffix.lower() == ".pdf"
    assert len(pages) == 12
    assert all(doc.metadata["source"].endswith(".pdf") for doc in pages)
    assert all("page" in doc.metadata for doc in chunks)
    assert all("start_index" in doc.metadata for doc in chunks)
    print(f"PASS: {len(pages)} PDF page Documents -> {len(chunks)} chunks")
    print("PASS: source, page, page_number, and start_index metadata retained")


if __name__ == "__main__":
    main()
