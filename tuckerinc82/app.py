from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI

from .backends import discover_backends
from .benchmarks import BenchmarkResult, aggregate
from .capabilities import discover_capabilities
from .event_bus import DataEvent, EventBus
from .event_ledger import EventLedger
from .evidence import EvidenceEnvelope, EVIDENCE_ROOT, append_evidence, content_hash
from .fabric import DataRecord
from .guardrails import GuardrailRequest, evaluate_guardrails
from .ingestion import AuthoritativeIngestor
from .self_healing import propose_remediation
from .source_mesh import enabled_sources
from .tucker_ai import TuckerExperiment

ROOT = Path(__file__).resolve().parents[1]
EVENT_LEDGER = EventLedger(ROOT / "data" / "events" / "events.ndjson")
EVENT_BUS = EventBus(ledger=EVENT_LEDGER)
INGESTOR = AuthoritativeIngestor()

app = FastAPI(
    title="Tucker AI",
    description="Standalone hybrid quantum-classical AI and authoritative data-fabric gateway.",
    version="0.7.0",
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "tucker-ai"}


@app.get("/api/sources")
def sources() -> dict[str, object]:
    registered = [source.model_dump(mode="json") for source in enabled_sources()]
    return {"count": len(registered), "sources": registered}


@app.post("/api/ingestion/source/{source_id}")
def ingest_source(source_id: str) -> dict[str, object]:
    source = next((item for item in enabled_sources() if item.source_id == source_id), None)
    if source is None:
        raise ValueError(f"unknown or disabled source: {source_id}")
    path = INGESTOR.ingest(source)
    return {"source_id": source_id, "evidence_path": str(path.relative_to(EVIDENCE_ROOT))}


@app.get("/api/tucker-ai/capabilities")
def quantum_capabilities() -> dict[str, object]:
    backends = discover_backends()
    return {"count": len(backends), "backends": backends}


@app.get("/api/tucker-ai/capability-discovery")
def capability_discovery() -> dict[str, object]:
    return discover_capabilities()


@app.post("/api/tucker-ai/guardrails/evaluate")
def evaluate_tucker_guardrails(request: GuardrailRequest) -> dict[str, object]:
    return evaluate_guardrails(request).model_dump(mode="json")


@app.post("/api/tucker-ai/experiments/validate")
def validate_tucker_experiment(experiment: TuckerExperiment) -> dict[str, object]:
    return experiment.model_dump(mode="json")


@app.post("/api/records/validate")
def validate_record(record: DataRecord) -> dict[str, object]:
    return record.with_integrity().model_dump(mode="json")


@app.post("/api/evidence/append")
def append_evidence_record(envelope: EvidenceEnvelope) -> dict[str, object]:
    path = append_evidence(envelope)
    return {"path": str(path.relative_to(EVIDENCE_ROOT)), "content_hash": content_hash(envelope.payload)}


@app.post("/api/events/publish")
def publish_event(event: DataEvent) -> dict[str, object]:
    return {"accepted": EVENT_BUS.publish(event), "event_id": event.event_id, "bus": EVENT_BUS.snapshot()}


@app.post("/api/events/replay-dlq")
def replay_dead_letters(limit: int = 100) -> dict[str, object]:
    return {"replayed": EVENT_BUS.replay_dlq(limit), "bus": EVENT_BUS.snapshot()}


@app.get("/api/events/status")
def event_status() -> dict[str, object]:
    return EVENT_BUS.snapshot()


@app.post("/api/remediation/propose")
def remediation_proposal(target: str, message: str, retryable: bool = False) -> dict[str, object]:
    return propose_remediation(target, RuntimeError(message), retryable=retryable).model_dump(mode="json")


@app.post("/api/benchmarks/aggregate")
def benchmark_aggregate(results: list[BenchmarkResult]) -> dict[str, float]:
    return aggregate(results)


@app.get("/api/data-fabric/clock")
def fabric_clock() -> dict[str, str]:
    return {"utc": datetime.now(timezone.utc).isoformat()}
