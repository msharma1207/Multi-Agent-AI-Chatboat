from app.services.analytics_service import AnalyticsService
from app.services.organization_service import OrganizationService


def test_organization_service_creates_workspace() -> None:
    service = OrganizationService()
    workspace = service.create_workspace("acme", "team")
    assert workspace["name"] == "team"


def test_analytics_service_tracks_usage() -> None:
    service = AnalyticsService()
    summary = service.get_summary()
    assert summary["total_events"] >= 0
