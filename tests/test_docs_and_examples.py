from app.services.docs_service import DocsService


def test_docs_service_lists_examples() -> None:
    service = DocsService()
    examples = service.list_examples()
    assert "chat" in examples
    assert "upload" in examples
