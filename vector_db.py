"""Compatibility imports; new code lives in the qdrant package."""

from qdrant.client import create_qdrant_client
from qdrant.collection import create_vector_store


__all__ = ["create_qdrant_client", "create_vector_store"]
