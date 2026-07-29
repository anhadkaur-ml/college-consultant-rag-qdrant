"""Create a Qdrant Cloud or local persistent client."""

from qdrant_client import QdrantClient

from config import Settings, settings


def create_qdrant_client(config: Settings = settings) -> QdrantClient:
    config.validate(require_google=False)
    if config.qdrant_mode == "cloud":
        return QdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            timeout=60,
        )

    config.qdrant_local_path.mkdir(parents=True, exist_ok=True)
    return QdrantClient(path=str(config.qdrant_local_path))
