from app.services.rag_service import RAGService
from app.services.workflow_service import WorkflowService


def test_rag_service_indexes_and_searches_documents() -> None:
    service = RAGService()
    service.add_document("alpha", "The capital of France is Paris")
    results = service.search("France")

    assert results[0]["text"] == "The capital of France is Paris"


def test_workflow_service_suggests_agent_sequence() -> None:
    service = WorkflowService()
    plan = service.plan("Summarize a document and answer a question")

    assert "research" in plan
    assert "rag" in plan
