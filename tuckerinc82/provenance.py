from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProvenanceEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provenance_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    retrieved_at: datetime
    source_revision: str | None = None
    parent_provenance_ids: list[str] = Field(default_factory=list)
    transformation: str = Field(min_length=1)
    input_hash: str = Field(min_length=64, max_length=64)
    output_hash: str = Field(min_length=64, max_length=64)


def make_provenance_id(source_id: str, payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(f"{source_id}:{canonical}".encode("utf-8")).hexdigest()
    return digest


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
