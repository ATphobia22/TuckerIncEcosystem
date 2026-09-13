from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OpenVikingBoundary:
    """External-service boundary for OpenViking; no AGPL source is vendored."""

    service_url: str
    protocol: str = "viking://"
    license_boundary: str = "external-service"

    def resource_uri(self, path: str) -> str:
        normalized = path.strip("/")
        if not normalized:
            raise ValueError("path must not be empty")
        return f"{self.protocol}{normalized}"
