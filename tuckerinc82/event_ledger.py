from __future__ import annotations

import json
from pathlib import Path
from threading import RLock
from typing import Iterable

from .event_bus import DataEvent


class EventLedger:
    """Append-only NDJSON ledger used as the durable replay boundary for events."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()

    def append(self, event: DataEvent) -> None:
        line = json.dumps(event.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
        with self._lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()

    def replay(self) -> Iterable[DataEvent]:
        if not self.path.exists():
            return
        with self._lock, self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield DataEvent.model_validate(json.loads(line))
