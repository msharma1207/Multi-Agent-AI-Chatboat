from fastapi import APIRouter

from app.schemas.organization import WorkspaceCreate
from app.services.organization_service import OrganizationService

router = APIRouter()
service = OrganizationService()


@router.post("/workspaces")
def create_workspace(payload: WorkspaceCreate) -> dict[str, object]:
    return service.create_workspace(payload.organization, payload.name)
