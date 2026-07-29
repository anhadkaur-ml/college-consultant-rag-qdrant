"""Create the Qdrant collection and LangChain vector-store wrapper."""

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PayloadSchemaType, VectorParams

from config import Settings, settings


def ensure_collection(
    client: QdrantClient,
    embeddings: GoogleGenerativeAIEmbeddings,
    config: Settings = settings,
) -> int:
    vector_size = len(embeddings.embed_query("collection dimension check"))
    if not client.collection_exists(config.qdrant_collection):
        client.create_collection(
            collection_name=config.qdrant_collection,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    collection = client.get_collection(config.qdrant_collection)
    payload_schema = collection.payload_schema or {}
    if "metadata.document_key" not in payload_schema:
        client.create_payload_index(
            collection_name=config.qdrant_collection,
            field_name="metadata.document_key",
            field_schema=PayloadSchemaType.KEYWORD,
            wait=True,
        )
    return vector_size


def create_vector_store(
    client: QdrantClient,
    embeddings: GoogleGenerativeAIEmbeddings,
    config: Settings = settings,
) -> QdrantVectorStore:
    ensure_collection(client, embeddings, config)
    return QdrantVectorStore(
        client=client,
        collection_name=config.qdrant_collection,
        embedding=embeddings,
    )
