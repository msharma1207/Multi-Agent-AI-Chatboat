from app.services.tool_service import ToolService


def test_tool_service_executes_calculator_and_filesystem_tools() -> None:
    service = ToolService()
    assert service.run_tool("calculator", "2 + 2") == 4
    assert service.run_tool("filesystem", "echo") == "filesystem-ready"
