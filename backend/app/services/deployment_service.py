from __future__ import annotations

class DeploymentService:
    """Simple deployment planning service for Docker and AWS targets."""

    def list_targets(self) -> list[str]:
        return ["docker", "aws"]
