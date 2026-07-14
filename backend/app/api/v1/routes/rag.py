from fastapi import APIRouter

from app.services.rag_service import RAGService

router = APIRouter()
service = RAGService()


@router.post("/documents")
def add_document(doc_id: str, text: str) -> dict[str, object]:
    return service.add_document(doc_id, text)


@router.get("/search")
def search_documents(query: str) -> list[dict[str, object]]:
    return service.search(query)
