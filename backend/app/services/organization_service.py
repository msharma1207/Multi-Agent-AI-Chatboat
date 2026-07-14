from __future__ import annotations

from typing import Any


class OrganizationService:
    """Simple workspace and organization management service."""

    def create_workspace(self, organization: str, name: str) -> dict[str, Any]:
        return {"organization": organization, "name": name, "status": "created"}
