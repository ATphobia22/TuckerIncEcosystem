from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

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


def canonical_https_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme.lower() != "https" or not parsed.netloc:
        raise ValueError("registered source URLs must use HTTPS")
    return urlunsplit(("https", parsed.netloc.lower(), parsed.path or "/", parsed.query, ""))


def is_registered_https_url(source_id: str, url: str) -> bool:
    """Require the requested URL to exactly match the registered endpoint."""
    source = get_source(source_id)
    registered = str(source.get("endpoint", ""))
    try:
        return canonical_https_url(url) == canonical_https_url(registered)
    except ValueError:
        return False
