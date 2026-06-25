"""Runtime configuration, loaded from the environment.

Nothing here has a real secret default — secrets come from the environment
(.env locally, a secret manager in the cloud). See .env.example at the repo root.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RECURVE_",
        env_file=".env",
        extra="ignore",
    )

    # app-metadata Postgres (the control plane)
    database_url: str = "postgresql+psycopg://recurve:recurve@localhost:5432/recurve"

    # local warehouse — DuckDB file; swapped for BigQuery in the live deploy
    warehouse_path: str = "data/local/recurve.duckdb"

    # Fernet key used to encrypt connection credentials at rest.
    # Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    fernet_key: str = ""

    # CORS — the Next.js app origin(s) allowed to call this API
    allowed_origins: list[str] = ["http://localhost:3000"]

    environment: str = "local"


@lru_cache
def get_settings() -> Settings:
    return Settings()
