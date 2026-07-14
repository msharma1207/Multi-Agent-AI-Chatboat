from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("", summary="Return configured providers")
def list_settings() -> dict[str, object]:
    return {
        "app_name": settings.app_name,
        "providers": {
            "openai": bool(settings.openai_api_key),
            "anthropic": bool(settings.anthropic_api_key),
            "gemini": bool(settings.gemini_api_key),
            "groq": bool(settings.groq_api_key),
            "ollama": True,
            "openrouter": bool(settings.openrouter_api_key),
            "huggingface": bool(settings.huggingface_api_key),
        },
        "ollama_base_url": settings.ollama_base_url,
    }
