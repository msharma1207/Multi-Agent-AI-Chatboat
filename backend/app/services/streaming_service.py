from __future__ import annotations

from typing import Any


class StreamingService:
    """Small helper for chunking text into stream-friendly segments."""

    def chunk_text(self, text: str, *, chunk_size: int = 20) -> list[str]:
        if not text:
            return []
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    def build_stream(self, text: str, *, chunk_size: int = 20) -> list[dict[str, Any]]:
        return [{"chunk": chunk, "index": index} for index, chunk in enumerate(self.chunk_text(text, chunk_size=chunk_size))]
