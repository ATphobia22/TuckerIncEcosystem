from datetime import datetime, timedelta, timezone

from tuckerinc82.fabric import DataRecord, FreshnessClass, compute_sha256, freshness_state


def test_hash_is_deterministic():
    payload = b'{"value":42}'
    assert compute_sha256(payload) == compute_sha256(payload)
    assert len(compute_sha256(payload)) == 64


def test_freshness_marks_recent_record_current():
    observed_at = datetime.now(timezone.utc) - timedelta(seconds=30)
    assert freshness_state(observed_at, ttl_seconds=120) == FreshnessClass.CURRENT


def test_freshness_marks_old_record_expired():
    observed_at = datetime.now(timezone.utc) - timedelta(seconds=300)
    assert freshness_state(observed_at, ttl_seconds=120) == FreshnessClass.EXPIRED


def test_data_record_requires_explicit_source_identity():
    record = DataRecord(
        source_id="usgs-03378500",
        source_url="https://waterservices.usgs.gov/",
        retrieved_at=datetime.now(timezone.utc),
        observed_at=datetime.now(timezone.utc),
        cadence="near_realtime",
        schema_version="1.0",
        geographic_scope="Posey County, Indiana",
        payload={"stage_ft": 376.4},
    )
    assert record.source_id == "usgs-03378500"
    assert record.freshness == FreshnessClass.CURRENT
