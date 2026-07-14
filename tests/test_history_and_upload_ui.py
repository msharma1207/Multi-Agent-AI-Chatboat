from app.services.history_service import HistoryService
from app.services.upload_ui_service import UploadUIService


def test_history_service_stores_messages() -> None:
    service = HistoryService()
    service.add_message("user", "hello")
    assert service.get_history()[0]["content"] == "hello"


def test_history_service_persists_conversation_lifecycle(tmp_path) -> None:
    path = tmp_path / "history.json"
    service = HistoryService(path)
    conversation = service.create_conversation("First chat", "coding")
    service.add_conversation_message(conversation["id"], "user", "hello")

    reloaded = HistoryService(path)
    saved = reloaded.get_conversation(conversation["id"])
    assert saved is not None
    assert saved["messages"][0]["content"] == "hello"
    assert reloaded.list_conversations()[0]["message_count"] == 1

    reloaded.rename_conversation(conversation["id"], "Renamed")
    assert reloaded.get_conversation(conversation["id"])["title"] == "Renamed"
    assert reloaded.delete_conversation(conversation["id"]) is True
    assert reloaded.get_conversation(conversation["id"]) is None


def test_upload_ui_service_builds_payload() -> None:
    service = UploadUIService()
    payload = service.build_payload("notes.txt")
    assert payload["filename"] == "notes.txt"
