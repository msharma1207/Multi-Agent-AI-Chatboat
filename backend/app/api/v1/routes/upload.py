from fastapi import APIRouter, UploadFile

from app.services.upload_service import UploadService

router = APIRouter()
service = UploadService()


@router.post("")
async def upload_file(file: UploadFile) -> dict[str, object]:
    content = await file.read()
    return service.process_upload(file.filename or "upload.bin", content)
