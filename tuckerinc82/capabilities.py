from __future__ import annotations

import platform
from typing import Any

from .quantum_adapters import discover_adapters


def discover_capabilities() -> dict[str, Any]:
    adapters = discover_adapters()
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "adapters": adapters,
        "available_count": sum(1 for adapter in adapters if adapter.get("available")),
    }
