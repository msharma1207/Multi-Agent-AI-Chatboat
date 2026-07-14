# AI Chat Platform

This workspace contains the initial production-ready scaffold for a multi-agent AI platform with:

- FastAPI backend
- Auth and chat endpoints
- LangGraph orchestration hooks
- Frontend shell
- Docker and documentation scaffolding

## Quick start

1. Create and activate the virtual environment
2. Install dependencies
3. Run the backend

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

In another terminal, start the interface:

```bash
cd frontend
npm install
npm run dev
```

## OpenRouter setup

Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY`. The browser only sends
the selected model ID to FastAPI; the secret key remains on the backend. The default
model is `openrouter/auto` and can be changed with `OPENROUTER_DEFAULT_MODEL`.

## Free-tier model strategy

The scaffold is designed to work with low-friction providers first:

- Ollama for local, no-key development
- Groq for low-cost inference and free credits
- OpenRouter for multi-provider gateway access
- HuggingFace for experimentation
- OpenAI, Anthropic, and Gemini are wired as configurable options via environment variables
