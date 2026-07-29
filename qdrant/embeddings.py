"""Embedding model used by the Qdrant vector store."""

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import Settings, settings


def create_embeddings(
    config: Settings = settings,
) -> GoogleGenerativeAIEmbeddings:
    config.validate(require_google=True)
    return GoogleGenerativeAIEmbeddings(
        model=config.embedding_model,
        google_api_key=config.google_api_key,
    )
