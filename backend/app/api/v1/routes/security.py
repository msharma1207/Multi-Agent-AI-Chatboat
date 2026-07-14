from fastapi import APIRouter

from app.services.security_service import SecurityService

router = APIRouter()
service = SecurityService()


@router.get("/mask")
def mask_secret(value: str) -> dict[str, str]:
    return {"masked": service.mask_secret(value)}
