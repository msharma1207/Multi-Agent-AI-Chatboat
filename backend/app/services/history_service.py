from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


class HistoryService:
    """Persist conversations and messages in a replaceable JSON-backed store."""

    def __init__(self, storage_path: str | Path | None = None) -> None:
        self.storage_path = Path(storage_path) if storage_path else None
        self.messages: list[dict[str, Any]] = []
        if self.storage_path:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict[str, Any]:
        if not self.storage_path or not self.storage_path.exists():
            return {"conversations": []}
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {"conversations": []}
        except (json.JSONDecodeError, OSError):
            return {"conversations": []}

    def _save(self, data: dict[str, Any]) -> None:
        if not self.storage_path:
            return
        temporary = self.storage_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(self.storage_path)

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def create_conversation(self, title: str = "New chat", mode: str = "chat") -> dict[str, Any]:
        data = self._load()
        now = self._now()
        conversation = {
            "id": uuid4().hex,
            "title": title.strip()[:80] or "New chat",
            "mode": mode,
            "created_at": now,
            "updated_at": now,
            "messages": [],
        }
        data["conversations"].insert(0, conversation)
        self._save(data)
        return conversation

    def list_conversations(self) -> list[dict[str, Any]]:
        conversations = self._load()["conversations"]
        conversations.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        return [
            {key: value for key, value in item.items() if key != "messages"}
            | {"message_count": len(item.get("messages", []))}
            for item in conversations
        ]

    def get_conversation(self, conversation_id: str) -> dict[str, Any] | None:
        return next(
            (item for item in self._load()["conversations"] if item.get("id") == conversation_id),
            None,
        )

    def add_conversation_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        image_data: str | None = None,
    ) -> dict[str, Any] | None:
        data = self._load()
        conversation = next(
            (item for item in data["conversations"] if item.get("id") == conversation_id),
            None,
        )
        if not conversation:
            return None
        message = {"role": role, "content": content, "created_at": self._now()}
        if image_data:
            message["image_data"] = image_data
        conversation["messages"].append(message)
        conversation["updated_at"] = self._now()
        self._save(data)
        return message

    def rename_conversation(self, conversation_id: str, title: str) -> dict[str, Any] | None:
        data = self._load()
        conversation = next(
            (item for item in data["conversations"] if item.get("id") == conversation_id),
            None,
        )
        if not conversation:
            return None
        conversation["title"] = title.strip()[:80] or conversation["title"]
        conversation["updated_at"] = self._now()
        self._save(data)
        return conversation

    def delete_conversation(self, conversation_id: str) -> bool:
        data = self._load()
        original = len(data["conversations"])
        data["conversations"] = [
            item for item in data["conversations"] if item.get("id") != conversation_id
        ]
        if len(data["conversations"]) == original:
            return False
        self._save(data)
        return True

    # Backwards-compatible flat history methods used by the original API/tests.
    def add_message(self, role: str, content: str) -> dict[str, Any]:
        message = {"role": role, "content": content}
        self.messages.append(message)
        return message

    def get_history(self) -> list[dict[str, Any]]:
        return self.messages
