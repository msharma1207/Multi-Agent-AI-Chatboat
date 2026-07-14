from __future__ import annotations

from typing import Any


class RAGService:
    """A lightweight in-memory retrieval service for phase 3 development."""

    def __init__(self) -> None:
        self.documents: list[dict[str, Any]] = []

    def add_document(self, doc_id: str, text: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        document = {"id": doc_id, "text": text, "metadata": metadata or {}}
        self.documents.append(document)
        return document

    def search(self, query: str, limit: int = 3) -> list[dict[str, Any]]:
        query_lower = query.lower()
        matches = [
            document
            for document in self.documents
            if query_lower in document["text"].lower()
        ]
        return matches[:limit]
