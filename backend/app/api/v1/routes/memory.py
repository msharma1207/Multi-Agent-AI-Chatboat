from fastapi import APIRouter

router = APIRouter()


@router.post("/store")
def store_memory(key: str, value: str) -> dict[str, str]:
    return {"key": key, "value": value}
