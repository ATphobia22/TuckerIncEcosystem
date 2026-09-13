from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


def is_due(source: dict[str, Any], *, last_retrieved_at: datetime | None, now: datetime | None = None) -> bool:
    """Return whether a registered source should be polled based on its TTL."""
    if not source.get("enabled", False):
        return False
    ttl_seconds = source.get("ttl_seconds")
    if not isinstance(ttl_seconds, int) or ttl_seconds < 1:
        return False
    if last_retrieved_at is None:
        return True
    current_time = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return current_time >= last_retrieved_at.astimezone(timezone.utc) + timedelta(seconds=ttl_seconds)
