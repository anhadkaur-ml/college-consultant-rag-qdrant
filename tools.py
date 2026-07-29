"""LangChain tool exposed to the college consultant agent."""

from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_qdrant import QdrantVectorStore

from services import retrieve_documents


def _format_document(document: Document) -> str:
    source = document.metadata.get("source_name", "unknown PDF")
    page = document.metadata.get("page_number", "?")
    return f"Source: {source}, page {page}\n{document.page_content}"


def build_knowledge_base_tool(vector_store: QdrantVectorStore):
    @tool(
        "search_college_knowledge_base",
        response_format="content_and_artifact",
    )
    def search_college_knowledge_base(query: str):
        """Search the college prospectus for facts relevant to a question."""
        documents = retrieve_documents(vector_store, query, k=4)
        return "\n\n".join(map(_format_document, documents)), documents

    return search_college_knowledge_base
