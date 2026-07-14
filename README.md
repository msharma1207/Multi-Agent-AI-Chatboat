# NexoraAI

NexoraAI is a full-stack, multi-model AI workspace for conversational assistance, coding, live web research, document analysis, presentation planning, image generation, and persistent chat memory.

## Features

- OpenRouter-powered model routing
- Auto and general chat modes
- Qwen3 Coder Next for coding tasks
- Perplexity Sonar for current web research with citations
- Document-aware prompts and text-file attachments
- Presentation outlines with slide notes and visual suggestions
- OpenRouter image-generation integration
- Intent-aware live-information routing
- Compact conversational context and persistent chat history
- Rename, restore, and delete conversations
- Markdown rendering, tables, code blocks, and Markdown copying
- Browser voice input
- Responsive dark interface
- FastAPI REST API with OpenAPI documentation

## Technology

- **Frontend:** Next.js 14, React 18, TypeScript
- **Backend:** FastAPI, Pydantic v2, HTTPX
- **AI gateway:** OpenRouter
- **Testing:** Pytest and TypeScript compiler checks
- **Deployment:** Docker and Docker Compose scaffolding

## Project structure

```text
backend/             FastAPI application, routes, services, and schemas
frontend/            Next.js user interface
tests/               Backend unit and integration tests
docs/                Architecture, API, and deployment documentation
docker/              Container image configuration
storage/             Local runtime persistence (contents are not committed)
```

## Local setup

### 1. Clone and enter the repository

```bash
git clone https://github.com/msharma1207/Multi-Agent-AI-Chatboat.git
cd Multi-Agent-AI-Chatboat
```

### 2. Configure Python

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure OpenRouter

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Set your server-side key:

```env
APP_NAME=NexoraAI
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_DEFAULT_MODEL=openrouter/auto
OPENROUTER_SITE_URL=http://localhost:3000
OPENROUTER_APP_NAME=NexoraAI
```

Never expose the OpenRouter key through a `NEXT_PUBLIC_` variable or commit `.env`.

### 4. Start the backend

```powershell
uvicorn app.main:app --reload --app-dir backend
```

Backend URLs:

- API: `http://localhost:8000`
- OpenAPI: `http://localhost:8000/docs`
- Health: `http://localhost:8000/api/v1/health`

### 5. Start the frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Model routing

| Mode | Default routing |
|---|---|
| Auto | OpenRouter Auto; switches to Sonar for time-sensitive requests |
| Chat | OpenRouter Auto; switches to Sonar when live information is required |
| Coding | Qwen3 Coder Next, with optional web search for current technical details |
| PDF | OpenRouter Auto with document-analysis instructions |
| PPT | OpenRouter Auto with presentation-design instructions |
| Image | Gemini 3.1 Flash Lite Image through OpenRouter |
| Search | Perplexity Sonar live research with citations |

Image generation and live search may consume OpenRouter credits.

## Tests

Run backend tests:

```powershell
.\env\Scripts\python.exe -m pytest tests -q
```

Run frontend type checking:

```powershell
cd frontend
npx tsc --noEmit
```

## Security

- API keys remain server-side.
- Local environment files, databases, histories, build output, and dependencies are ignored by Git.
- Generated chat history is stored locally under `storage/` during development.
- Production deployments should use managed secrets, restricted CORS origins, HTTPS, PostgreSQL, and Redis.

## Current limitations

- Binary PDF extraction is not connected yet; text-based documents are supported.
- PPT mode generates presentation content but not a downloadable `.pptx` file.
- Image generation requires sufficient OpenRouter credits.
- Browser voice input depends on browser support and microphone permission.

## License

See [LICENSE](LICENSE).
