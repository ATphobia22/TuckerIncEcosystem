from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ComponentClassification:
    path: str
    category: str
    confidence: float
    reason: str


def classify_paths(paths: list[str]) -> list[ComponentClassification]:
    rules = (
        ("connector", ("connector", "adapter", "ingest", "source")),
        ("event", ("event", "bus", "queue", "dlq")),
        ("evidence", ("evidence", "provenance", "ledger", "fabric")),
        ("quantum", ("quantum", "qiskit", "cirq", "pennylane", "qml")),
        ("governance", ("guardrail", "policy", "govern", "security")),
        ("test", ("test", "spec", "benchmark")),
        ("documentation", ("docs", "readme", ".md")),
    )
    results: list[ComponentClassification] = []
    for path in paths:
        normalized = path.lower()
        category, confidence, reason = "utility", 0.50, "No specialized classification rule matched."
        for candidate, tokens in rules:
            if any(token in normalized for token in tokens):
                category, confidence = candidate, 0.90
                reason = f"Matched repository-intelligence token for {candidate}."
                break
        results.append(ComponentClassification(path, category, confidence, reason))
    return results


def manifest(classifications: list[ComponentClassification]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "components": [
            {
                "path": item.path,
                "category": item.category,
                "confidence": item.confidence,
                "reason": item.reason,
            }
            for item in classifications
        ],
    }


def write_manifest(classifications: list[ComponentClassification], path: Path | None = None) -> Path:
    target = path or ROOT / "data" / "intelligence" / "component_manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest(classifications), indent=2, sort_keys=True), encoding="utf-8")
    return target
