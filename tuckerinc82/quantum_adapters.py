from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Protocol

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_REGISTRY = ROOT / "data" / "quantum" / "adapter_registry.json"


class QuantumAdapter(Protocol):
    backend_id: str

    def capabilities(self) -> list[str]: ...

    def validate(self, circuit: dict[str, Any]) -> dict[str, Any]: ...


class RegistryAdapter:
    def __init__(self, metadata: dict[str, Any], available: bool) -> None:
        self.metadata = metadata
        self.backend_id = str(metadata["backend_id"])
        self.available = available

    def capabilities(self) -> list[str]:
        return list(self.metadata.get("capabilities", []))

    def validate(self, circuit: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(circuit, dict):
            raise TypeError("circuit must be a JSON object")
        return {
            "backend_id": self.backend_id,
            "available": self.available,
            "accepted": True,
            "operation_count": len(circuit.get("operations", [])) if isinstance(circuit.get("operations", []), list) else 0,
        }


def _load_registry() -> list[dict[str, Any]]:
    document = json.loads(ADAPTER_REGISTRY.read_text(encoding="utf-8"))
    adapters = document.get("adapters", [])
    if not isinstance(adapters, list):
        raise ValueError("adapter registry must contain an 'adapters' list")
    return adapters


def create_adapter(backend_id: str) -> RegistryAdapter:
    for metadata in _load_registry():
        if metadata.get("backend_id") != backend_id:
            continue
        modules = [item for item in metadata.get("modules", []) if isinstance(item, str)]
        available = any(importlib.util.find_spec(module) is not None for module in modules)
        return RegistryAdapter(metadata, available)
    raise KeyError(f"unknown quantum backend: {backend_id}")


def discover_adapters() -> list[dict[str, Any]]:
    return [
        {**metadata, "available": any(importlib.util.find_spec(module) is not None for module in metadata.get("modules", []))}
        for metadata in _load_registry()
    ]
