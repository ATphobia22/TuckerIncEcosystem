from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI

from .fabric import DataRecord

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "sources" / "source_registry.json"

app = FastAPI(
    title="TuckerInc.82 Data Fabric",
    description="Standalone cross-project integration and authoritative data-fabric gateway.",
    version="0.2.0",
)


def load_source_registry() -> list[dict[str, Any]]:
    if not REGISTRY_PATH.exists():
        return []
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    sources = document.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("source registry must contain a list named 'sources'")
    return sources


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "tuckerinc82-data-fabric"}


@app.get("/api/sources")
def sources() -> dict[str, Any]:
    registered = load_source_registry()
    return {"count": len(registered), "sources": registered}


@app.post("/api/records/validate")
def validate_record(record: DataRecord) -> dict[str, Any]:
    return record.with_integrity().model_dump(mode="json")
