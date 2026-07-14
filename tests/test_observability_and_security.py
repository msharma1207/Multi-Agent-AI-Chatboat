from app.services.observability_service import ObservabilityService
from app.services.security_service import SecurityService


def test_observability_service_logs_event() -> None:
    service = ObservabilityService()
    record = service.log_event("chat", "message")
    assert record["event"] == "chat"


def test_security_service_masks_secret() -> None:
    service = SecurityService()
    masked = service.mask_secret("sk-123456")
    assert masked == "sk-******"
