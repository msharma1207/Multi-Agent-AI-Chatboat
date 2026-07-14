from __future__ import annotations

from typing import Any


class UploadUIService:
    """Build simple upload payloads for frontend-driven file uploads."""

    def build_payload(self, filename: str) -> dict[str, Any]:
        return {"filename": filename, "upload_mode": "direct"}
