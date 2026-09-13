from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "sources" / "source_registry.json"


def load_registry() -> dict[str, Any]:
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        registry = json.load(handle)
    if not isinstance(registry, dict) or not isinstance(registry.get("sources"), list):
        raise ValueError("invalid source registry")
    return registry


def get_source(source_id: str) -> dict[str, Any]:
    for source in load_registry()["sources"]:
        if source.get("source_id") == source_id:
            return source
    raise KeyError(f"unknown source: {source_id}")


def is_registered_https_url(source_id: str, url: str) -> bool:
    source = get_source(source_id)
    registered = str(source.get("endpoint", ""))
    requested = urlparse(url)
    expected = urlparse(registered)
    return (
        requested.scheme == "https"
        and expected.scheme == "https"
        and requested.netloc == expected.netloc
    )
