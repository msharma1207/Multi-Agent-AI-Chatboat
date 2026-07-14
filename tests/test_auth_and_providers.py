from pathlib import Path

from app.services.auth_service import AuthService
from app.services.provider_service import ProviderService
from app.api.v1.routes.chat import needs_live_information


def test_signup_and_login_flow(tmp_path: Path) -> None:
    service = AuthService(db_path=tmp_path / "auth.db")

    user = service.signup("demo@example.com", "secret123", "Demo")
    assert user["email"] == "demo@example.com"

    tokens = service.login("demo@example.com", "secret123")
    assert tokens["access_token"]
    assert tokens["refresh_token"]

    refreshed = service.refresh(tokens["refresh_token"])
    assert refreshed["access_token"]


def test_provider_service_builds_ollama_payload() -> None:
    service = ProviderService()
    payload = service.build_request("Hello", provider="ollama", model="llama3.2")

    assert payload["model"] == "llama3.2"
    assert payload["messages"][0]["content"] == "Hello"


def test_provider_service_builds_compact_conversation_context() -> None:
    service = ProviderService()
    payload = service.build_request(
        "What is my project called?",
        provider="openrouter",
        model="openrouter/auto",
        system_prompt="Be concise.",
        history=[
            {"role": "user", "content": "My project is called NexoraAI."},
            {"role": "assistant", "content": "Understood."},
        ],
        max_tokens=512,
    )

    assert [message["role"] for message in payload["messages"]] == [
        "system",
        "user",
        "assistant",
        "user",
    ]
    assert payload["messages"][-1]["content"] == "What is my project called?"
    assert payload["max_tokens"] == 512


def test_live_information_intent_detection() -> None:
    assert needs_live_information("What is the latest stable Python release?") is True
    assert needs_live_information("What is the weather today?") is True
    assert needs_live_information("Explain how Python decorators work") is False
    assert needs_live_information("Review my current variable naming") is False
