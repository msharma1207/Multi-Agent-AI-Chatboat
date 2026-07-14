from fastapi import APIRouter

from app.services.deployment_service import DeploymentService
from app.services.policy_service import PolicyService

router = APIRouter()
deployment_service = DeploymentService()
policy_service = PolicyService()


@router.get("/targets")
def list_targets() -> dict[str, object]:
    return {"targets": deployment_service.list_targets()}


@router.get("/security-headers")
def get_security_headers() -> dict[str, str]:
    return policy_service.get_security_headers()
