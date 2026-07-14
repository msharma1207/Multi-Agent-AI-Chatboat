from fastapi import APIRouter

from app.services.persistence_service import PersistenceService

router = APIRouter()
service = PersistenceService()


@router.post("/state")
def save_state(key: str, value: str) -> dict[str, object]:
    service.save_state(key, {"value": value})
    return {"status": "saved", "key": key}


@router.get("/state")
def load_state(key: str) -> dict[str, object]:
    return service.load_state(key)
