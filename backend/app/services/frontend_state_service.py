from __future__ import annotations

from typing import Any


class FrontendStateService:
    """Simple in-memory state service for the frontend chat experience."""

    def __init__(self) -> None:
        self.messages: list[str] = []

    def add_message(self, message: str) -> None:
        self.messages.append(message)

    def get_state(self) -> dict[str, Any]:
        return {"messages": self.messages}
