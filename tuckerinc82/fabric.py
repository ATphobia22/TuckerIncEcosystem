from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FreshnessClass(StrEnum):
    CURRENT = "current"
    STALE = "stale"
    EXPIRED = "expired"
    UNKNOWN = "unknown"


class DataRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    retrieved_at: datetime
    observed_at: datetime | None = None
    cadence: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    geographic_scope: str = Field(min_length=1)
    payload: dict[str, Any]
    content_hash: str | None = None
    freshness: FreshnessClass = FreshnessClass.UNKNOWN

    @field_validator("retrieved_at", "observed_at")
    @classmethod
    def require_utc(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("timestamps must be timezone-aware")
        return value.astimezone(timezone.utc)

    def with_integrity(self) -> "DataRecord":
        canonical_payload = json.dumps(
            self.payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        return self.model_copy(update={"content_hash": compute_sha256(canonical_payload)})


def compute_sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def freshness_state(
    observed_at: datetime | None,
    ttl_seconds: int,
    now: datetime | None = None,
) -> FreshnessClass:
    if observed_at is None or ttl_seconds < 0:
        return FreshnessClass.UNKNOWN

    current_time = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    observed_time = observed_at.astimezone(timezone.utc)
    age_seconds = (current_time - observed_time).total_seconds()

    if age_seconds < 0:
        return FreshnessClass.UNKNOWN
    if age_seconds <= ttl_seconds:
        return FreshnessClass.CURRENT
    if age_seconds <= ttl_seconds * 3:
        return FreshnessClass.STALE
    return FreshnessClass.EXPIRED
