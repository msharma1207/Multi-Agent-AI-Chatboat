from __future__ import annotations

from typing import Any


class UploadService:
    """Process uploaded files for later indexing or storage."""

    def process_upload(self, filename: str, content: bytes) -> dict[str, Any]:
        text = content.decode("utf-8", errors="ignore")
        content_type = "text/plain"
        if filename.endswith(".json"):
            content_type = "application/json"

        return {
            "filename": filename,
            "size": len(content),
            "content_type": content_type,
            "preview": text[:200],
        }
