from app.services.vector_service import VectorService
from app.services.config_service import ConfigService


def test_vector_service_indexes_and_searches() -> None:
    service = VectorService()
    service.index_document("doc-1", "Paris is the capital of France")
    results = service.search("France")
    assert results[0]["id"] == "doc-1"


def test_config_service_reads_defaults() -> None:
    service = ConfigService()
    assert service.get("postgres_host") == "localhost"
