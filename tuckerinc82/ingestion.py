from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .fabric import DataRecord, FreshnessClass, freshness_state


class IngestionError(RuntimeError):
    """Raised when an external source cannot be safely ingested."""


def fetch_json_source(
    *,
    source_id: str,
    source_url: str,
    cadence: str,
    schema_version: str,
    geographic_scope: str,
    ttl_seconds: int,
    timeout_seconds: float = 10.0,
    user_agent: str = "TuckerInc.82/0.2",
) -> DataRecord:
    request = Request(
        source_url,
        headers={"Accept": "application/json", "User-Agent": user_agent},
        method="GET",
    )
    retrieved_at = datetime.now(timezone.utc)
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            raw_payload = response.read()
    except (HTTPError, URLError, TimeoutError) as exc:
        raise IngestionError(f"source fetch failed for {source_id}") from exc

    try:
        payload: dict[str, Any] = json.loads(raw_payload)
    except json.JSONDecodeError as exc:
        raise IngestionError(f"source returned invalid JSON for {source_id}") from exc

    record = DataRecord(
        source_id=source_id,
        source_url=source_url,
        retrieved_at=retrieved_at,
        observed_at=retrieved_at,
        cadence=cadence,
        schema_version=schema_version,
        geographic_scope=geographic_scope,
        payload=payload,
        freshness=freshness_state(retrieved_at, ttl_seconds, retrieved_at),
    )
    return record.with_integrity()
