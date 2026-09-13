from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "sources" / "source_registry.json"


class SourceEndpoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    url: str = Field(min_length=1)
    authority: str = Field(min_length=1)
    cadence: str = Field(min_length=1)
    enabled: bool = True
    tags: list[str] = Field(default_factory=list)

    @property
    def host(self) -> str:
        parsed = urlparse(self.url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("authoritative source endpoints must use HTTPS URLs")
        return parsed.hostname.lower()


def load_sources() -> list[SourceEndpoint]:
    if not REGISTRY.exists():
        return []
    document: dict[str, Any] = json.loads(REGISTRY.read_text(encoding="utf-8"))
    raw = document.get("sources", [])
    if not isinstance(raw, list):
        raise ValueError("source registry must contain a list named 'sources'")
    return [SourceEndpoint.model_validate(item) for item in raw]


def enabled_sources() -> list[SourceEndpoint]:
    return [source for source in load_sources() if source.enabled]
