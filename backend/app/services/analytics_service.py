from __future__ import annotations

from typing import Any


class AnalyticsService:
    """Minimal analytics summary service for admin dashboards."""

    def get_summary(self) -> dict[str, Any]:
        return {"total_events": 0, "active_users": 0, "messages_today": 0}
