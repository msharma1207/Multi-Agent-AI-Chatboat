from datetime import date
import re

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.agent_orchestrator import orchestrate_agent_flow
from app.services.history_service import HistoryService
from app.services.provider_registry import get_provider_registry
from app.services.provider_service import ProviderService

router = APIRouter()
provider_service = ProviderService()
history_service = HistoryService("storage/chat_history.json")


def needs_live_information(message: str) -> bool:
    """Detect requests whose answer is likely to have changed since training."""
    pattern = re.compile(
        r"\b(latest|today|right now|recent|recently|news|weather|forecast|"
        r"price|stock|score|schedule|breaking|this week|this month|"
        r"current (?:version|release|president|prime minister|ceo|law|rate|"
        r"status|events?|exchange rate))\b",
        re.IGNORECASE,
    )
    return bool(pattern.search(message))

MODE_CONFIG = {
    "auto": {
        "model": "openrouter/auto",
        "max_tokens": 2048,
        "prompt": "Choose the best response style and be concise, accurate, and practical.",
    },
    "chat": {
        "model": "openrouter/auto",
        "max_tokens": 2048,
        "prompt": "You are CortexAI, a helpful conversational assistant.",
    },
    "coding": {
        "model": "qwen/qwen3-coder-next",
        "max_tokens": 4096,
        "prompt": "You are a senior software engineer. Provide correct, secure code with concise explanations and runnable examples.",
    },
    "pdf": {
        "model": "openrouter/auto",
        "max_tokens": 4096,
        "prompt": "You are a document analyst. Analyze supplied document text, summarize it, answer questions, and clearly state when source content is missing.",
    },
    "ppt": {
        "model": "openrouter/auto",
        "max_tokens": 4096,
        "prompt": "You are a presentation designer. Produce a slide-by-slide outline with titles, concise bullets, speaker notes, and visual suggestions.",
    },
    "image": {
        "model": "google/gemini-3.1-flash-lite-image",
        "prompt": "Generate a polished image that follows the user's description.",
    },
    "search": {
        "model": "perplexity/sonar",
        "max_tokens": 2048,
        "prompt": f"Today is {date.today().isoformat()}. You are a live web research assistant. Always search current sources before answering, state relevant dates explicitly, and cite authoritative sources with links. Never answer current-information questions only from training memory.",
    },
}


@router.post("", response_model=ChatResponse)
def create_chat(payload: ChatRequest) -> ChatResponse:
    orchestrate_agent_flow("chat", payload.message)
    provider = payload.provider or "openrouter"
    mode = (payload.mode or "chat").lower()
    config = MODE_CONFIG.get(mode, MODE_CONFIG["chat"])
    model = str(config["model"]) if provider == "openrouter" else (payload.model or "llama3.2")
    system_prompt = str(config.get("prompt", ""))
    tools = config.get("tools")
    if provider == "openrouter" and mode != "search" and needs_live_information(payload.message):
        system_prompt += f" Today is {date.today().isoformat()}. Search live sources before answering and cite them."
        if mode in {"auto", "chat"}:
            model = "perplexity/sonar"
        else:
            tools = [{"type": "openrouter:web_search"}]
    history: list[dict[str, str]] = []
    if payload.conversation_id:
        conversation = history_service.get_conversation(payload.conversation_id)
        if conversation:
            saved = conversation.get("messages", [])
            if saved and saved[-1].get("role") == "user":
                latest = str(saved[-1].get("content", ""))
                if payload.message.startswith(latest):
                    saved = saved[:-1]
            for item in saved[-8:]:
                role = item.get("role")
                content = str(item.get("content", ""))[-2000:]
                if role in {"user", "assistant"} and content:
                    history.append({"role": role, "content": content})

    if provider == "openrouter" and mode == "image":
        image_data = provider_service.send_image(payload.message, model=model)
        if image_data.startswith("Provider "):
            return ChatResponse(reply=image_data, model=model, provider=provider, mode=mode)
        return ChatResponse(
            reply="Image generated from your prompt.",
            model=model,
            provider=provider,
            mode=mode,
            image_data=image_data,
        )

    reply = provider_service.send_request(
        payload.message,
        provider=provider,
        model=model,
        system_prompt=f"{system_prompt} Use prior conversation context only when relevant. Answer concisely by default unless the user requests detail.",
        tools=tools,
        max_tokens=int(config.get("max_tokens", 2048)),
        history=history,
    )
    if mode == "search" and "http" not in reply.lower() and not reply.startswith("Provider "):
        reply += "\n\nNo verifiable live source was returned. Please refine the search query and try again."
    return ChatResponse(reply=reply, model=model, provider=provider, mode=mode)


@router.get("/modes")
def list_chat_modes() -> list[dict[str, str]]:
    return [{"mode": mode, "model": str(config["model"])} for mode, config in MODE_CONFIG.items()]


@router.get("/providers")
def list_chat_providers() -> list[dict[str, object]]:
    return [
        {"name": provider.name, "enabled": provider.enabled, "notes": provider.notes}
        for provider in get_provider_registry()
    ]
