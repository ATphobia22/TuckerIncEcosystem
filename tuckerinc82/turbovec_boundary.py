from __future__ import annotations

import importlib.util
from typing import Any, Protocol


class ContextIndex(Protocol):
    def add(self, vectors: Any) -> None: ...
    def search(self, query: Any, k: int = 10) -> tuple[Any, Any]: ...


class TurboVecBoundary:
    """Optional context-index boundary; core runtime never imports turbovec eagerly."""

    backend_id = "turbovec"

    def __init__(self, dimension: int | None = None, bit_width: int = 4) -> None:
        self.dimension = dimension
        self.bit_width = bit_width
        self._index: ContextIndex | None = None

    @property
    def available(self) -> bool:
        return importlib.util.find_spec("turbovec") is not None

    def initialize(self) -> None:
        if not self.available:
            raise RuntimeError("optional turbovec dependency is not installed")
        from turbovec import TurboQuantIndex

        self._index = TurboQuantIndex(dim=self.dimension, bit_width=self.bit_width)

    def add(self, vectors: Any) -> None:
        if self._index is None:
            raise RuntimeError("TurboVecBoundary.initialize() must be called first")
        self._index.add(vectors)

    def search(self, query: Any, k: int = 10) -> tuple[Any, Any]:
        if self._index is None:
            raise RuntimeError("TurboVecBoundary.initialize() must be called first")
        if k < 1:
            raise ValueError("k must be positive")
        return self._index.search(query, k=k)
