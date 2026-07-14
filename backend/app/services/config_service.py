from __future__ import annotations

from typing import Any


class ConfigService:
    """Simple configuration service for database and cache settings."""

    def __init__(self) -> None:
        self.defaults: dict[str, Any] = {
            "postgres_host": "localhost",
            "postgres_port": 5432,
            "postgres_db": "ai_platform",
            "redis_host": "localhost",
            "redis_port": 6379,
            "qdrant_host": "localhost",
            "qdrant_port": 6333,
        }

    def get(self, key: str) -> Any:
        return self.defaults.get(key)
