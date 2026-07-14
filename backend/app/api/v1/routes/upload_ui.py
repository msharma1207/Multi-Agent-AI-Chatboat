from fastapi import APIRouter

from app.services.upload_ui_service import UploadUIService

router = APIRouter()
service = UploadUIService()


@router.post("/prepare")
def prepare_upload(filename: str) -> dict[str, object]:
    return service.build_payload(filename)
