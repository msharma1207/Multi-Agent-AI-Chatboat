from fastapi import APIRouter

from app.services.vector_service import VectorService

router = APIRouter()
service = VectorService()


@router.post("/index")
def index_document(doc_id: str, text: str) -> dict[str, object]:
    return service.index_document(doc_id, text)


@router.get("/search")
def search_vector(query: str) -> list[dict[str, object]]:
    return service.search(query)
