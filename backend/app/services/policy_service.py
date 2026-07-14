from __future__ import annotations

class PolicyService:
    """Security policy helpers for production deployment defaults."""

    def get_security_headers(self) -> dict[str, str]:
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
