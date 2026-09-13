from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "quantum" / "backend_registry.json"


def load_backend_registry() -> list[dict[str, Any]]:
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    backends = document.get("backends", [])
    if not isinstance(backends, list):
        raise ValueError("quantum backend registry must contain a list named 'backends'")
    return backends


def discover_backends() -> list[dict[str, Any]]:
    discovered: list[dict[str, Any]] = []
    for backend in load_backend_registry():
        modules = backend.get("modules", [])
        available = any(
            isinstance(module, str) and importlib.util.find_spec(module) is not None
            for module in modules
        )
        discovered.append({**backend, "available": available})
    return discovered
