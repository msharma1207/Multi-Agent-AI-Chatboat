from fastapi import APIRouter

from app.services.analytics_service import AnalyticsService

router = APIRouter()
service = AnalyticsService()


@router.get("/summary")
def get_summary() -> dict[str, object]:
    return service.get_summary()
