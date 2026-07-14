from app.services.frontend_state_service import FrontendStateService


def test_frontend_state_service_tracks_conversation() -> None:
    service = FrontendStateService()
    service.add_message("hello")
    state = service.get_state()
    assert state["messages"][0] == "hello"
