from __future__ import annotations

class DocsService:
    """Helpful documentation service for example flows and API usage."""

    def list_examples(self) -> list[str]:
        return ["chat", "upload", "rag", "workflow"]
