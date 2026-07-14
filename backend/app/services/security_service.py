from __future__ import annotations


class SecurityService:
    """Utility helpers for secret masking and basic validation."""

    def mask_secret(self, value: str) -> str:
        if len(value) <= 3:
            return "*" * len(value)
        return value[:3] + "*" * max(0, len(value) - 3)
