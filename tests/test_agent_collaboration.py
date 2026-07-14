from app.services.agent_collaboration_service import AgentCollaborationService


def test_agent_collaboration_service_routes_to_workers() -> None:
    service = AgentCollaborationService()
    plan = service.plan("Summarize and answer a question")
    assert "supervisor" in plan
    assert "research" in plan
