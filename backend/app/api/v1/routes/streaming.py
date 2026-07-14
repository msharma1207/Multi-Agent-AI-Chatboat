from fastapi import APIRouter

from app.services.streaming_service import StreamingService

router = APIRouter()
service = StreamingService()


@router.post("/chunks")
def stream_text(text: str) -> dict[str, object]:
    return {"chunks": service.build_stream(text)}
