from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI

from .backends import discover_backends
from .fabric import DataRecord
from .guardrails import GuardrailRequest, evaluate_guardrails
from .tucker_ai import TuckerExperiment

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "sources" / "source_registry.json"

app = FastAPI(
    title="Tucker AI",
    description="Standalone hybrid quantum-classical AI and authoritative data-fabric gateway.",
    version="0.3.0",
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
    return {"status": "ok", "service": "tucker-ai"}


@app.get("/api/sources")
def sources() -> dict[str, Any]:
    registered = load_source_registry()
    return {"count": len(registered), "sources": registered}


@app.get("/api/tucker-ai/capabilities")
def quantum_capabilities() -> dict[str, Any]:
    backends = discover_backends()
    return {"count": len(backends), "backends": backends}


@app.post("/api/tucker-ai/guardrails/evaluate")
def evaluate_tucker_guardrails(request: GuardrailRequest) -> dict[str, Any]:
    return evaluate_guardrails(request).model_dump(mode="json")


@app.post("/api/tucker-ai/experiments/validate")
def validate_tucker_experiment(experiment: TuckerExperiment) -> dict[str, Any]:
    return experiment.model_dump(mode="json")


@app.post("/api/records/validate")
def validate_record(record: DataRecord) -> dict[str, Any]:
    return record.with_integrity().model_dump(mode="json")
