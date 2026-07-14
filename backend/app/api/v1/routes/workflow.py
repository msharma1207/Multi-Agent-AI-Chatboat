from fastapi import APIRouter

from app.services.workflow_service import WorkflowService

router = APIRouter()
service = WorkflowService()


@router.post("/plan")
def plan_workflow(request: str) -> dict[str, object]:
    return {"request": request, "plan": service.plan(request)}
