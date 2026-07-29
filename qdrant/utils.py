"""Stable identifiers and fingerprints for idempotent Qdrant seeding."""

import hashlib
from pathlib import Path
import uuid

from langchain_core.documents import Document


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def create_point_id(document_key: str, chunk: Document) -> str:
    stable_value = "|".join(
        (
            document_key,
            str(chunk.metadata.get("page", "")),
            str(chunk.metadata.get("start_index", "")),
            hashlib.sha256(chunk.page_content.encode("utf-8")).hexdigest(),
        )
    )
    return str(uuid.uuid5(uuid.NAMESPACE_URL, stable_value))
