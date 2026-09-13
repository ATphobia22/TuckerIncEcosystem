from __future__ import annotations

import hashlib
import json
import threading
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field


class DataEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    occurred_at: datetime
    payload: dict[str, Any]
    evidence_hash: str | None = None
    schema_version: str = "1.0"

    def canonical_bytes(self) -> bytes:
        return json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":")).encode()

    def fingerprint(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


@dataclass(frozen=True)
class DeadLetter:
    event: DataEvent
    error: str
    failed_at: datetime


Handler = Callable[[DataEvent], None]


class EventBus:
    """Bounded, deterministic in-process event bus with deduplication and replayable DLQ."""

    def __init__(self, max_queue: int = 10_000) -> None:
        if max_queue < 1:
            raise ValueError("max_queue must be positive")
        self._queue: deque[DataEvent] = deque(maxlen=max_queue)
        self._seen: set[str] = set()
        self._handlers: dict[str, list[Handler]] = {}
        self._dlq: list[DeadLetter] = []
        self._lock = threading.RLock()

    def subscribe(self, event_type: str, handler: Handler) -> None:
        if not event_type:
            raise ValueError("event_type is required")
        with self._lock:
            self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: DataEvent) -> bool:
        key = event.event_id
        with self._lock:
            if key in self._seen:
                return False
            self._seen.add(key)
            self._queue.append(event)
        self._dispatch(event)
        return True

    def _dispatch(self, event: DataEvent) -> None:
        for handler in tuple(self._handlers.get(event.event_type, [])):
            try:
                handler(event)
            except Exception as exc:  # noqa: BLE001 - failure is captured for replay
                with self._lock:
                    self._dlq.append(DeadLetter(event, f"{type(exc).__name__}: {exc}", datetime.now(timezone.utc)))

    def replay_dlq(self, limit: int = 100) -> int:
        if limit < 1:
            return 0
        with self._lock:
            candidates = self._dlq[:limit]
            self._dlq = self._dlq[limit:]
        for item in candidates:
            self._dispatch(item.event)
        return len(candidates)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "queued": len(self._queue),
                "deduplicated": len(self._seen),
                "dead_lettered": len(self._dlq),
                "event_types": sorted(self._handlers),
            }
