from __future__ import annotations

import hashlib
from pathlib import Path


class EvidenceStore:
    """Content-addressed immutable raw evidence store for local deployments."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, payload: bytes) -> str:
        digest = hashlib.sha256(payload).hexdigest()
        destination = self.root / digest[:2] / f"{digest}.bin"
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            return digest
        temporary = destination.with_suffix(".tmp")
        temporary.write_bytes(payload)
        temporary.replace(destination)
        return digest

    def get(self, digest: str) -> bytes:
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise ValueError("invalid SHA-256 evidence identifier")
        path = self.root / digest[:2] / f"{digest}.bin"
        return path.read_bytes()
