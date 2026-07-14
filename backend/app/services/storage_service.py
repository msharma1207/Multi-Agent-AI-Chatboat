from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StorageService:
    """A lightweight storage abstraction that can later be backed by PostgreSQL or Redis."""

    def __init__(self, storage_dir: str | Path | None = None) -> None:
        self.storage_dir = Path(storage_dir or "./storage")
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_document(self, key: str, value: dict[str, Any]) -> None:
        target = self.storage_dir / f"{key}.json"
        target.write_text(json.dumps(value), encoding="utf-8")

    def get_document(self, key: str) -> dict[str, Any]:
        target = self.storage_dir / f"{key}.json"
        if not target.exists():
            return {}
        return json.loads(target.read_text(encoding="utf-8"))
