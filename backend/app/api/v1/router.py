from fastapi import APIRouter

from app.api.v1.routes.agent_collaboration import router as agent_collaboration_router
from app.api.v1.routes.analytics import router as analytics_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.chat import router as chat_router
from app.api.v1.routes.config import router as config_router
from app.api.v1.routes.deployment import router as deployment_router
from app.api.v1.routes.docs import router as docs_router
from app.api.v1.routes.frontend_state import router as frontend_state_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.history import router as history_router
from app.api.v1.routes.memory import router as memory_router
from app.api.v1.routes.observability import router as observability_router
from app.api.v1.routes.organization import router as organization_router
from app.api.v1.routes.persistence import router as persistence_router
from app.api.v1.routes.prompt_template import router as prompt_template_router
from app.api.v1.routes.rag import router as rag_router
from app.api.v1.routes.security import router as security_router
from app.api.v1.routes.settings import router as settings_router
from app.api.v1.routes.streaming import router as streaming_router
from app.api.v1.routes.tool import router as tool_router
from app.api.v1.routes.upload import router as upload_router
from app.api.v1.routes.upload_ui import router as upload_ui_router
from app.api.v1.routes.vector import router as vector_router
from app.api.v1.routes.workflow import router as workflow_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(settings_router, prefix="/settings", tags=["settings"])
api_router.include_router(rag_router, prefix="/rag", tags=["rag"])
api_router.include_router(workflow_router, prefix="/workflow", tags=["workflow"])
api_router.include_router(persistence_router, prefix="/persistence", tags=["persistence"])
api_router.include_router(upload_router, prefix="/upload", tags=["upload"])
api_router.include_router(streaming_router, prefix="/stream", tags=["stream"])
api_router.include_router(vector_router, prefix="/vector", tags=["vector"])
api_router.include_router(config_router, prefix="/config", tags=["config"])
api_router.include_router(observability_router, prefix="/observability", tags=["observability"])
api_router.include_router(security_router, prefix="/security", tags=["security"])
api_router.include_router(frontend_state_router, prefix="/frontend-state", tags=["frontend-state"])
api_router.include_router(history_router, prefix="/history", tags=["history"])
api_router.include_router(upload_ui_router, prefix="/upload-ui", tags=["upload-ui"])
api_router.include_router(tool_router, prefix="/tools", tags=["tools"])
api_router.include_router(agent_collaboration_router, prefix="/agent-collaboration", tags=["agent-collaboration"])
api_router.include_router(memory_router, prefix="/memory", tags=["memory"])
api_router.include_router(prompt_template_router, prefix="/prompt-template", tags=["prompt-template"])
api_router.include_router(deployment_router, prefix="/deployment", tags=["deployment"])
api_router.include_router(docs_router, prefix="/docs", tags=["docs"])
api_router.include_router(organization_router, prefix="/organizations", tags=["organizations"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
