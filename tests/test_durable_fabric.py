from __future__ import annotations

from datetime import datetime, timezone

from tuckerinc82.event_bus import DataEvent, EventBus
from tuckerinc82.event_ledger import EventLedger
from tuckerinc82.source_mesh import SourceEndpoint


def test_event_ledger_persists_and_replays(tmp_path) -> None:
    ledger = EventLedger(tmp_path / "events.ndjson")
    bus = EventBus(ledger=ledger)
    event = DataEvent(
        event_id="durable-1",
        event_type="source.updated",
        source_id="test-source",
        occurred_at=datetime.now(timezone.utc),
        payload={"value": 1},
    )
    assert bus.publish(event) is True
    replayed = list(ledger.replay())
    assert replayed[0].event_id == "durable-1"
    assert bus.snapshot()["durable"] is True


def test_source_mesh_requires_https() -> None:
    source = SourceEndpoint(
        source_id="x",
        name="x",
        authority="test",
        cadence="manual",
        endpoint="https://example.org/data",
    )
    assert source.host == "example.org"
