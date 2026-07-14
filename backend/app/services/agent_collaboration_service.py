from __future__ import annotations

from typing import Any


class AgentCollaborationService:
    """Coordinate supervisor and worker agents for multi-agent workflows."""

    def plan(self, request: str) -> list[str]:
        lowered = request.lower()
        plan = ["supervisor"]
        if "summarize" in lowered or "research" in lowered:
            plan.append("research")
        if "question" in lowered or "answer" in lowered:
            plan.append("rag")
        if "code" in lowered or "python" in lowered:
            plan.append("coding")
        return plan

    def execute(self, request: str) -> dict[str, Any]:
        return {"request": request, "agents": self.plan(request)}
