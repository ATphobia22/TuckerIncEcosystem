from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, build_opener

from .evidence import EvidenceEnvelope, append_evidence, content_hash
from .source_mesh import SourceEndpoint, enabled_sources


class NoRedirectHandler(__import__("urllib.request", fromlist=["HTTPRedirectHandler"]).HTTPRedirectHandler):
    def redirect_request(self, request: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        raise URLError(f"redirect rejected for authoritative source: {newurl}")


class AuthoritativeIngestor:
    def __init__(self, timeout_seconds: float = 15.0, max_bytes: int = 5_000_000) -> None:
        if timeout_seconds <= 0 or max_bytes <= 0:
            raise ValueError("timeout_seconds and max_bytes must be positive")
        self.timeout_seconds = timeout_seconds
        self.max_bytes = max_bytes
        self._opener = build_opener(NoRedirectHandler())

    def fetch(self, source: SourceEndpoint) -> EvidenceEnvelope:
        request = Request(
            source.endpoint,
            headers={"Accept": "application/json, text/plain, text/html;q=0.8", "User-Agent": "TuckerAI/0.6"},
            method="GET",
        )
        with self._opener.open(request, timeout=self.timeout_seconds) as response:
            if response.status != 200:
                raise RuntimeError(f"source returned HTTP {response.status}")
            if response.geturl() != source.endpoint:
                raise RuntimeError("authoritative source changed URL without explicit registry update")
            body = response.read(self.max_bytes + 1)
            if len(body) > self.max_bytes:
                raise ValueError("authoritative payload exceeds configured size limit")
            content_type = (response.headers.get("Content-Type") or "").split(";", 1)[0].lower()

        text = body.decode("utf-8", errors="replace")
        payload: dict[str, Any]
        if content_type == "application/json":
            decoded = json.loads(text)
            payload = decoded if isinstance(decoded, dict) else {"value": decoded}
        else:
            payload = {"content_type": content_type or "unknown", "body": text}

        return EvidenceEnvelope(
            source_id=source.source_id,
            source_url=source.endpoint,
            retrieved_at=datetime.now(timezone.utc),
            schema_version="1.0",
            payload=payload,
            content_hash=content_hash(payload),
        )

    def ingest(self, source: SourceEndpoint) -> Path:
        return append_evidence(self.fetch(source))

    def ingest_enabled(self) -> list[Path]:
        return [self.ingest(source) for source in enabled_sources()]
