from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class BenchmarkResult:
    benchmark_id: str
    quantum_metric: float
    classical_metric: float
    uncertainty: float
    quantum_resource_units: float
    simulator: bool
    notes: str = ""

    @property
    def relative_delta(self) -> float:
        if self.classical_metric == 0:
            return math.nan
        return (self.quantum_metric - self.classical_metric) / abs(self.classical_metric)


def validate_benchmark(result: BenchmarkResult) -> None:
    if result.uncertainty < 0:
        raise ValueError("uncertainty must be non-negative")
    if result.quantum_resource_units < 0:
        raise ValueError("quantum_resource_units must be non-negative")
    if not math.isfinite(result.quantum_metric) or not math.isfinite(result.classical_metric):
        raise ValueError("benchmark metrics must be finite")


def aggregate(results: Sequence[BenchmarkResult]) -> dict[str, float]:
    if not results:
        raise ValueError("at least one benchmark result is required")
    for result in results:
        validate_benchmark(result)
    return {
        "count": float(len(results)),
        "mean_quantum_metric": sum(r.quantum_metric for r in results) / len(results),
        "mean_classical_metric": sum(r.classical_metric for r in results) / len(results),
        "mean_uncertainty": sum(r.uncertainty for r in results) / len(results),
        "total_quantum_resource_units": sum(r.quantum_resource_units for r in results),
    }
