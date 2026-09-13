from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = ROOT / "data" / "evidence"


class EvidenceEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    retrieved_at: datetime
    schema_version: str = Field(min_length=1)
    payload: dict[str, Any]
    content_hash: str = Field(min_length=64, max_length=64)

    def utc(self) -> "EvidenceEnvelope":
        timestamp = self.retrieved_at
        if timestamp.tzinfo is None:
            raise ValueError("retrieved_at must be timezone-aware")
        return self.model_copy(update={"retrieved_at": timestamp.astimezone(timezone.utc)})


def canonical_json(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def content_hash(payload: Any) -> str:
    return hashlib.sha256(canonical_json(payload)).hexdigest()


def append_evidence(envelope: EvidenceEnvelope) -> Path:
    """Write immutable, content-addressed evidence without overwriting an existing object."""
    normalized = envelope.utc()
    expected = content_hash(normalized.payload)
    if expected != normalized.content_hash:
        raise ValueError("content_hash does not match canonical payload")
    target = EVIDENCE_ROOT / normalized.source_id / f"{normalized.content_hash}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        existing = json.loads(target.read_text(encoding="utf-8"))
        if existing != normalized.model_dump(mode="json"):
            raise ValueError("immutable evidence collision detected")
        return target
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(normalized.model_dump(mode="json"), sort_keys=True, indent=2), encoding="utf-8")
    temporary.replace(target)
    return target
