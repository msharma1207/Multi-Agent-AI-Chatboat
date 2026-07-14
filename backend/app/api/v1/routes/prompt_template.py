from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_template() -> dict[str, str]:
    return {"template": "You are a helpful AI assistant."}
