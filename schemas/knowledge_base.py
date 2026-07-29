"""Small typed result objects shared by the application."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SeedReport:
    status: str
    pages: int
    chunks: int
    collection: str
    document_fingerprint: str


@dataclass(frozen=True)
class SearchResult:
    content: str
    score: float
    source: str
    page: int
    page_number: int
    start_index: int | None
