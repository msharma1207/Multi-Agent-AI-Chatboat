from app.services.storage_service import StorageService
from app.services.streaming_service import StreamingService


def test_storage_service_can_store_and_fetch_documents() -> None:
    service = StorageService()
    service.save_document("doc-1", {"content": "hello"})
    assert service.get_document("doc-1") == {"content": "hello"}


def test_streaming_service_builds_chunks() -> None:
    service = StreamingService()
    chunks = service.chunk_text("hello world", chunk_size=5)
    assert len(chunks) >= 1
