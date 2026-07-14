from dataclasses import dataclass

from app.core.config import settings


@dataclass(slots=True)
class ProviderConfig:
    name: str
    enabled: bool
    notes: str


def get_provider_registry() -> list[ProviderConfig]:
    return [
        ProviderConfig(name="ollama", enabled=True, notes="Best free/local option for development"),
        ProviderConfig(name="groq", enabled=bool(settings.groq_api_key), notes="Low-cost inference with free credits"),
        ProviderConfig(name="openrouter", enabled=bool(settings.openrouter_api_key), notes="Access multiple providers through one gateway"),
        ProviderConfig(name="huggingface", enabled=bool(settings.huggingface_api_key), notes="Model hub support for experimental workloads"),
        ProviderConfig(name="openai", enabled=bool(settings.openai_api_key), notes="Requires API key"),
        ProviderConfig(name="anthropic", enabled=bool(settings.anthropic_api_key), notes="Requires API key"),
        ProviderConfig(name="gemini", enabled=bool(settings.gemini_api_key), notes="Requires API key"),
    ]
