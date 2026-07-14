from app.services.deployment_service import DeploymentService
from app.services.policy_service import PolicyService


def test_deployment_service_lists_targets() -> None:
    service = DeploymentService()
    targets = service.list_targets()
    assert "docker" in targets
    assert "aws" in targets


def test_policy_service_builds_headers() -> None:
    service = PolicyService()
    headers = service.get_security_headers()
    assert headers["X-Content-Type-Options"] == "nosniff"
