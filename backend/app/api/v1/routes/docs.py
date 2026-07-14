from fastapi import APIRouter

from app.services.docs_service import DocsService

router = APIRouter()
service = DocsService()


@router.get("/examples")
def get_examples() -> dict[str, object]:
    return {"examples": service.list_examples()}
