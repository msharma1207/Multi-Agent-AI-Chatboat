from fastapi import APIRouter

from app.services.observability_service import ObservabilityService

router = APIRouter()
service = ObservabilityService()


@router.post("/events")
def log_event(event: str, message: str) -> dict[str, object]:
    return service.log_event(event, message)
