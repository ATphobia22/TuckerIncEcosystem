from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChromePromptCapability:
    """Capability descriptor for Chrome's browser-managed Prompt API.

    This module intentionally does not invoke browser APIs from the Python server.
    The actual model call belongs in a secure browser client using the Web AI API.
    """

    api: str = "Prompt API"
    status: str = "browser-managed"
    client_only: bool = True
    server_fallback_required: bool = True


def capability_descriptor() -> dict[str, object]:
    capability = ChromePromptCapability()
    return {
        "api": capability.api,
        "status": capability.status,
        "client_only": capability.client_only,
        "server_fallback_required": capability.server_fallback_required,
        "security": "never expose secrets or trust unvalidated browser-generated instructions",
    }
