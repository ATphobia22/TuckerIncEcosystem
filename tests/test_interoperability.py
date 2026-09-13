from __future__ import annotations

from datetime import datetime, timezone

import pytest

from tuckerinc82.event_bus import DataEvent, EventBus
from tuckerinc82.evidence import EvidenceEnvelope, append_evidence, content_hash
from tuckerinc82.repository_intelligence import classify_paths


def test_event_bus_deduplicates_and_reports_failures() -> None:
    bus = EventBus()
    seen: list[str] = []
    bus.subscribe("test.event", lambda event: seen.append(event.event_id))
    event = DataEvent(
        event_id="evt-1",
        event_type="test.event",
        source_id="test",
        occurred_at=datetime.now(timezone.utc),
        payload={"value": 1},
    )
    assert bus.publish(event) is True
    assert bus.publish(event) is False
    assert seen == ["evt-1"]


def test_evidence_is_content_addressed(tmp_path: pytest.TempPathFactory) -> None:
    payload = {"b": 2, "a": 1}
    digest = content_hash(payload)
    envelope = EvidenceEnvelope(
        source_id="test-source",
        source_url="https://example.org/data",
        retrieved_at=datetime.now(timezone.utc),
        schema_version="1.0",
        payload=payload,
        content_hash=digest,
    )
    import tuckerinc82.evidence as evidence

    original = evidence.EVIDENCE_ROOT
    evidence.EVIDENCE_ROOT = tmp_path / "evidence"
    try:
        first = append_evidence(envelope)
        second = append_evidence(envelope)
        assert first == second
        assert first.exists()
    finally:
        evidence.EVIDENCE_ROOT = original


def test_repository_intelligence_classifies_quantum_and_events() -> None:
    results = classify_paths(["tuckerinc82/quantum_adapter.py", "tuckerinc82/event_bus.py"])
    assert [item.category for item in results] == ["quantum", "event"]
