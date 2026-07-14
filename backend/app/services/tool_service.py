from __future__ import annotations

from typing import Any


class ToolService:
    """Utility tools for agent workflows."""

    def run_tool(self, tool_name: str, input_value: str) -> Any:
        if tool_name == "calculator":
            try:
                return eval(input_value, {}, {})
            except Exception:
                return None

        if tool_name == "filesystem":
            return "filesystem-ready"

        if tool_name == "web_search":
            return f"search-results-for:{input_value}"

        if tool_name == "rest":
            return {"url": input_value, "status": "simulated"}

        return None
