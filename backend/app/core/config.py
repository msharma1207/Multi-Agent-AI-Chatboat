from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AI Platform"
    api_v1_prefix: str = "/api/v1"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    gemini_api_key: str | None = None
    groq_api_key: str | None = None
    ollama_base_url: str = "http://localhost:11434"
    openrouter_api_key: str | None = None
    openrouter_default_model: str = "openrouter/auto"
    openrouter_site_url: str = "http://localhost:3000"
    openrouter_app_name: str = "CortexAI"
    huggingface_api_key: str | None = None


settings = Settings()
