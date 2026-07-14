from __future__ import annotations

from typing import Any


class VectorService:
    """Lightweight vector-search service that mimics Qdrant-style document indexing."""

    def __init__(self) -> None:
        self.documents: list[dict[str, Any]] = []

    def index_document(self, doc_id: str, text: str) -> dict[str, Any]:
        document = {"id": doc_id, "text": text}
        self.documents.append(document)
        return document

    def search(self, query: str, limit: int = 3) -> list[dict[str, Any]]:
        query_lower = query.lower()
        matches = [document for document in self.documents if query_lower in document["text"].lower()]
        return matches[:limit]
