from fastapi import APIRouter

from app.services.frontend_state_service import FrontendStateService

router = APIRouter()
service = FrontendStateService()


@router.post("/messages")
def add_message(message: str) -> dict[str, object]:
    service.add_message(message)
    return service.get_state()


@router.get("")
def get_state() -> dict[str, object]:
    return service.get_state()
