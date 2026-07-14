from fastapi import APIRouter

from app.services.tool_service import ToolService

router = APIRouter()
service = ToolService()


@router.get("")
def list_tools() -> list[dict[str, str]]:
    return [
        {"name": "calculator", "kind": "math"},
        {"name": "filesystem", "kind": "local"},
        {"name": "web_search", "kind": "network"},
        {"name": "rest", "kind": "http"},
    ]


@router.post("/run")
def run_tool(tool_name: str, input_value: str) -> dict[str, object]:
    return {"tool": tool_name, "result": service.run_tool(tool_name, input_value)}
