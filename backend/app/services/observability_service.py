from __future__ import annotations

from typing import Any


class ObservabilityService:
    """A minimal observability layer for structured logs and metrics hooks."""

    def log_event(self, event: str, message: str) -> dict[str, Any]:
        return {"event": event, "message": message, "status": "logged"}
