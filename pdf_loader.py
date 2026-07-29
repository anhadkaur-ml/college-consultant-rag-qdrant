"""Load and split the college prospectus as LangChain Documents."""

from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from config import PROJECT_ROOT, Settings, settings


PDF_PATH = PROJECT_ROOT / "documents" / "college_database_prospectus.pdf"


def load_pdf_pages(pdf_path: str | Path) -> list[Document]:
    path = Path(pdf_path).resolve()
    if not path.is_file() or path.suffix.lower() != ".pdf":
        raise FileNotFoundError(f"PDF not found: {path}")

    documents: list[Document] = []
    for page_index, page in enumerate(PdfReader(path).pages):
        text = (page.extract_text() or "").strip()
        if text:
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(path),
                        "source_name": path.name,
                        "page": page_index,
                        "page_number": page_index + 1,
                    },
                )
            )
    if not documents:
        raise ValueError(f"No extractable text found in {path}")
    return documents


def load_college_pdf() -> list[Document]:
    """Load the configured college prospectus."""
    return load_pdf_pages(PDF_PATH)


def split_documents(
    documents: list[Document],
    config: Settings = settings,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        add_start_index=True,
    )
    chunks = splitter.split_documents(documents)
    for chunk_index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = chunk_index
    return chunks
