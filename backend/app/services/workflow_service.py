from __future__ import annotations

from typing import Any


class WorkflowService:
    """A LangGraph-inspired supervisor planner for phase 3 orchestration."""

    def plan(self, request: str) -> list[str]:
        lowered = request.lower()
        steps: list[str] = ["supervisor"]

        if "document" in lowered or "question" in lowered:
            steps.append("rag")

        if "summarize" in lowered or "analysis" in lowered:
            steps.append("research")

        if "code" in lowered or "python" in lowered:
            steps.append("coding")

        return steps

    def execute(self, request: str) -> dict[str, Any]:
        return {"request": request, "plan": self.plan(request)}
