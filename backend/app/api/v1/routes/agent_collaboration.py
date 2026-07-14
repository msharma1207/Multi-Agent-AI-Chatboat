from fastapi import APIRouter

from app.services.agent_collaboration_service import AgentCollaborationService

router = APIRouter()
service = AgentCollaborationService()


@router.post("/plan")
def plan_agents(request: str) -> dict[str, object]:
    return {"request": request, "agents": service.plan(request)}
