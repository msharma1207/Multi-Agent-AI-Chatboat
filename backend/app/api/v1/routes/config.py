from fastapi import APIRouter

from app.services.config_service import ConfigService

router = APIRouter()
service = ConfigService()


@router.get("")
def get_config() -> dict[str, object]:
    return {
        "postgres_host": service.get("postgres_host"),
        "postgres_port": service.get("postgres_port"),
        "redis_host": service.get("redis_host"),
        "redis_port": service.get("redis_port"),
        "qdrant_host": service.get("qdrant_host"),
        "qdrant_port": service.get("qdrant_port"),
    }
