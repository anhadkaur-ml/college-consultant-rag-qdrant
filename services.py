"""Application service for indexing and searching the PDF knowledge base."""

from pathlib import Path

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, PointIdsList

from config import Settings, settings
from models import create_chat_model
from pdf_loader import PDF_PATH, load_pdf_pages, split_documents
from qdrant.client import create_qdrant_client
from qdrant.collection import create_vector_store
from qdrant.embeddings import create_embeddings
from qdrant.utils import create_point_id, file_sha256
from schemas.knowledge_base import SearchResult, SeedReport
from schemas.outputs import ChatbotOutput


def build_vector_store(
    config: Settings = settings,
) -> tuple[QdrantClient, QdrantVectorStore]:
    client = create_qdrant_client(config)
    return client, create_vector_store(client, create_embeddings(config), config)


def seed_knowledge_base(
    pdf_path: Path = PDF_PATH,
    config: Settings = settings,
) -> SeedReport:
    pages = load_pdf_pages(pdf_path)
    chunks = split_documents(pages, config)
    client, vector_store = build_vector_store(config)
    document_key = pdf_path.resolve().name
    fingerprint = file_sha256(pdf_path)

    for chunk in chunks:
        chunk.metadata["document_key"] = document_key
        chunk.metadata["document_fingerprint"] = fingerprint
    ids = [create_point_id(document_key, chunk) for chunk in chunks]

    points, _ = client.scroll(
        collection_name=config.qdrant_collection,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="metadata.document_key",
                    match=MatchValue(value=document_key),
                )
            ]
        ),
        limit=10_000,
        with_payload=False,
        with_vectors=False,
    )
    existing_ids = {str(point.id) for point in points}
    expected_ids = set(ids)
    status = "already_seeded"
    if existing_ids != expected_ids:
        stale_ids = existing_ids - expected_ids
        if stale_ids:
            client.delete(
                collection_name=config.qdrant_collection,
                points_selector=PointIdsList(points=list(stale_ids)),
                wait=True,
            )
        vector_store.add_documents(documents=chunks, ids=ids)
        status = "seeded"

    return SeedReport(
        status=status,
        pages=len(pages),
        chunks=len(chunks),
        collection=config.qdrant_collection,
        document_fingerprint=fingerprint,
    )


def retrieve_documents(
    vector_store: QdrantVectorStore,
    query: str,
    *,
    k: int = 4,
) -> list[Document]:
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    ).invoke(query)


def search_knowledge_base(
    vector_store: QdrantVectorStore,
    query: str,
    *,
    k: int = 4,
) -> list[SearchResult]:
    return [
        SearchResult(
            content=document.page_content,
            score=float(score),
            source=str(
                document.metadata.get("source_name")
                or document.metadata.get("source", "unknown")
            ),
            page=int(document.metadata.get("page", -1)),
            page_number=int(document.metadata.get("page_number", 0)),
            start_index=document.metadata.get("start_index"),
        )
        for document, score in vector_store.similarity_search_with_score(
            query, k=k
        )
    ]


def get_ai_output(
    user_prompt: str,
    conversation_history: list[dict] | None = None,
) -> ChatbotOutput:
    """Run the retriever agent and return a structured answer."""
    from langchain.agents import create_agent
    from langchain.agents.structured_output import ToolStrategy

    from prompts import SYSTEM_PROMPT
    from tools import build_knowledge_base_tool

    if not user_prompt or not user_prompt.strip():
        raise ValueError("The user prompt cannot be empty.")

    _, vector_store = build_vector_store()
    agent = create_agent(
        model=create_chat_model(),
        tools=[build_knowledge_base_tool(vector_store)],
        system_prompt=SYSTEM_PROMPT,
        response_format=ToolStrategy(ChatbotOutput),
    )
    messages = list((conversation_history or [])[-10:])
    messages.append({"role": "user", "content": user_prompt.strip()})
    result = agent.invoke({"messages": messages})
    return result["structured_response"]
