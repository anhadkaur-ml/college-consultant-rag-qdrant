"""Environment-backed settings. Secrets are never stored in source code."""

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")
# The Google integration recognizes both names. This project intentionally
# uses GOOGLE_API_KEY, so discard a conflicting inherited legacy variable.
os.environ.pop("GEMINI_API_KEY", None)


@dataclass(frozen=True)
class Settings:
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    qdrant_mode: str = os.getenv("QDRANT_MODE", "cloud").strip().lower()
    qdrant_url: str | None = os.getenv("QDRANT_URL")
    qdrant_api_key: str | None = os.getenv("QDRANT_API_KEY")
    qdrant_local_path: Path = PROJECT_ROOT / os.getenv(
        "QDRANT_LOCAL_PATH", "data/qdrant_storage"
    )
    qdrant_collection: str = os.getenv(
        "QDRANT_COLLECTION", "college_prospectus"
    )
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "models/gemini-embedding-001"
    )
    chat_model: str = os.getenv("CHAT_MODEL", "gemini-3.6-flash")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    def validate(self, *, require_google: bool = True) -> None:
        if self.qdrant_mode not in {"cloud", "local"}:
            raise ValueError("QDRANT_MODE must be either 'cloud' or 'local'.")
        if self.qdrant_mode == "cloud":
            missing = [
                name
                for name, value in {
                    "QDRANT_URL": self.qdrant_url,
                    "QDRANT_API_KEY": self.qdrant_api_key,
                }.items()
                if not value
            ]
            if missing:
                raise ValueError(
                    "Missing cloud setting(s): " + ", ".join(missing)
                )
        if require_google and not self.google_api_key:
            raise ValueError("Missing GOOGLE_API_KEY in .env.")


settings = Settings()
