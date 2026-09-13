from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .fabric import DataRecord, freshness_state
from .registry import is_registered_https_url


class IngestionError(RuntimeError):
    """Raised when an external source cannot be safely ingested."""


MAX_PAYLOAD_BYTES = 5 * 1024 * 1024


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
    parsed = urlparse(source_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise IngestionError("only HTTPS sources are permitted")
    if not is_registered_https_url(source_id, source_url):
        raise IngestionError(f"URL is not registered for source {source_id}")
    if timeout_seconds <= 0 or timeout_seconds > 60:
        raise IngestionError("timeout_seconds must be between 0 and 60")

    request = Request(
        source_url,
        headers={"Accept": "application/json", "User-Agent": user_agent},
        method="GET",
    )
    retrieved_at = datetime.now(timezone.utc)
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > MAX_PAYLOAD_BYTES:
                raise IngestionError("source payload exceeds configured size limit")
            raw_payload = response.read(MAX_PAYLOAD_BYTES + 1)
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        raise IngestionError(f"source fetch failed for {source_id}") from exc

    if len(raw_payload) > MAX_PAYLOAD_BYTES:
        raise IngestionError("source payload exceeds configured size limit")

    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError as exc:
        raise IngestionError(f"source returned invalid JSON for {source_id}") from exc
    if not isinstance(payload, dict):
        raise IngestionError("top-level source payload must be a JSON object")

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
