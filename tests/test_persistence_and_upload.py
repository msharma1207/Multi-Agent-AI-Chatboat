from app.services.persistence_service import PersistenceService
from app.services.upload_service import UploadService


def test_persistence_service_stores_and_reads_state() -> None:
    service = PersistenceService()
    service.save_state("chat:1", {"message": "hi"})
    assert service.load_state("chat:1") == {"message": "hi"}


def test_upload_service_accepts_text_payload() -> None:
    service = UploadService()
    result = service.process_upload("notes.txt", b"Hello world")
    assert result["filename"] == "notes.txt"
    assert result["content_type"] == "text/plain"
