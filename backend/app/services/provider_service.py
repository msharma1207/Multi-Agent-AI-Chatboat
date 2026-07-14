from typing import Any

import httpx

from app.core.config import settings


class ProviderService:
    """Build provider-specific payloads for supported free-tier backends."""

    def build_request(
        self,
        prompt: str,
        *,
        provider: str = "ollama",
        model: str = "llama3.2",
        system_prompt: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        max_tokens: int | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        if provider == "huggingface":
            return {"inputs": prompt}

        if provider == "anthropic":
            return {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            }

        if provider == "openai":
            return {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            }

        if provider == "gemini":
            return {"prompt": prompt}

        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
        }
        if tools and provider == "openrouter":
            payload["tools"] = tools
        if max_tokens:
            payload["max_tokens"] = max_tokens
        return payload

    def get_request_config(self, provider: str, model: str) -> tuple[str, dict[str, str]]:
        if provider == "ollama":
            return f"{settings.ollama_base_url}/v1/chat/completions", {"Content-Type": "application/json"}

        if provider == "openrouter":
            if not settings.openrouter_api_key:
                raise ValueError("OpenRouter API key is not configured")
            return (
                "https://openrouter.ai/api/v1/chat/completions",
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "HTTP-Referer": settings.openrouter_site_url,
                    "X-OpenRouter-Title": settings.openrouter_app_name,
                },
            )

        if provider == "groq":
            if not settings.groq_api_key:
                raise ValueError("Groq API key is not configured")
            return (
                "https://api.groq.com/v1/experimental/2024-10-25/completions",
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.groq_api_key}",
                },
            )

        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key is not configured")
            return (
                "https://api.openai.com/v1/chat/completions",
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.openai_api_key}",
                },
            )

        if provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key is not configured")
            return (
                "https://api.anthropic.com/v1/chat/completions",
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.anthropic_api_key}",
                },
            )

        if provider == "huggingface":
            if not settings.huggingface_api_key:
                raise ValueError("HuggingFace API key is not configured")
            return (
                f"https://api-inference.huggingface.co/models/{model}",
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.huggingface_api_key}",
                },
            )

        if provider == "gemini":
            if not settings.gemini_api_key:
                raise ValueError("Gemini API key is not configured")
            return (
                f"https://gemini.googleapis.com/v1/models/{model}:generateText",
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.gemini_api_key}",
                },
            )

        raise ValueError(f"Unsupported provider: {provider}")

    def parse_response(self, response_data: dict[str, Any], provider: str) -> str:
        if provider == "ollama":
            if completion := response_data.get("completion"):
                return completion
            if choices := response_data.get("choices"):
                first_choice = choices[0] if isinstance(choices, list) and choices else None
                if first_choice and isinstance(first_choice, dict):
                    return first_choice.get("message", {}).get("content", "") or first_choice.get("text", "")
            return str(response_data)

        if provider in {"openrouter", "groq", "openai", "anthropic"}:
            if choices := response_data.get("choices"):
                first_choice = choices[0] if isinstance(choices, list) and choices else None
                if first_choice and isinstance(first_choice, dict):
                    if message := first_choice.get("message"):
                        content = message.get("content", "")
                        annotations = message.get("annotations", [])
                        citations: list[str] = []
                        citation_links: list[str] = []
                        for annotation in annotations if isinstance(annotations, list) else []:
                            citation = annotation.get("url_citation", {}) if isinstance(annotation, dict) else {}
                            url = citation.get("url")
                            title = citation.get("title") or url
                            if url and url not in citations and url not in content:
                                citations.append(url)
                                citation_links.append(f"- [{title}]({url})")
                        if citation_links:
                            content = content.rstrip() + "\n\n**Sources**\n" + "\n".join(citation_links)
                        return content
                    return first_choice.get("text", "")
            if completion := response_data.get("completion"):
                return completion
            if text := response_data.get("text"):
                return text
            return str(response_data)

        if provider == "huggingface":
            if isinstance(response_data, dict):
                if generated_text := response_data.get("generated_text"):
                    return generated_text
                if outputs := response_data.get("outputs"):
                    first_output = outputs[0] if isinstance(outputs, list) and outputs else None
                    if isinstance(first_output, dict):
                        return first_output.get("generated_text", "") or str(first_output)
            return str(response_data)

        if provider == "gemini":
            if candidates := response_data.get("candidates"):
                first_candidate = candidates[0] if isinstance(candidates, list) and candidates else None
                if first_candidate and isinstance(first_candidate, dict):
                    return first_candidate.get("output", "")
            return str(response_data)

        return str(response_data)

    def send_request(
        self,
        prompt: str,
        *,
        provider: str = "ollama",
        model: str = "llama3.2",
        system_prompt: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        max_tokens: int | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        url, headers = self.get_request_config(provider, model)
        payload = self.build_request(
            prompt,
            provider=provider,
            model=model,
            system_prompt=system_prompt,
            tools=tools,
            max_tokens=max_tokens,
            history=history,
        )

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return self.parse_response(response.json(), provider)
        except httpx.HTTPStatusError as exc:
            return f"Provider error ({provider}): {exc.response.status_code} {exc.response.text}"
        except Exception as exc:
            return f"Provider request failed ({provider}): {exc}"

    def send_image(self, prompt: str, *, model: str) -> str:
        """Generate one image and return it as a browser-ready data URL."""
        _, headers = self.get_request_config("openrouter", model)
        payload = {
            "model": model,
            "prompt": prompt,
            "n": 1,
            "resolution": "1K",
            "aspect_ratio": "1:1",
            "output_format": "png",
        }
        try:
            with httpx.Client(timeout=120.0) as client:
                response = client.post(
                    "https://openrouter.ai/api/v1/images",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                item = response.json().get("data", [{}])[0]
                encoded = item.get("b64_json")
                if not encoded:
                    raise ValueError("OpenRouter returned no image data")
                media_type = item.get("media_type") or "image/png"
                return f"data:{media_type};base64,{encoded}"
        except httpx.HTTPStatusError as exc:
            return f"Provider error (openrouter image): {exc.response.status_code} {exc.response.text}"
        except Exception as exc:
            return f"Provider request failed (openrouter image): {exc}"
