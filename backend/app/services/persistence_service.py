from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PersistenceService:
    """A simple persistence layer for chat state and session data."""

    def __init__(self, storage_dir: str | Path | None = None) -> None:
        self.storage_dir = Path(storage_dir or "./storage")
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_state(self, key: str, value: dict[str, Any]) -> None:
        target = self.storage_dir / f"{key.replace('/', '_')}.json"
        target.write_text(json.dumps(value), encoding="utf-8")

    def load_state(self, key: str) -> dict[str, Any]:
        target = self.storage_dir / f"{key.replace('/', '_')}.json"
        if not target.exists():
            return {}
        return json.loads(target.read_text(encoding="utf-8"))
