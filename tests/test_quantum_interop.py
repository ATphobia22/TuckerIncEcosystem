from __future__ import annotations

from datetime import datetime, timezone

from tuckerinc82.benchmarks import BenchmarkResult, aggregate
from tuckerinc82.capabilities import discover_capabilities
from tuckerinc82.quantum_adapters import create_adapter
from tuckerinc82.self_healing import RemediationAction, propose_remediation


def test_adapter_factory_is_provider_neutral() -> None:
    adapter = create_adapter("qiskit")
    result = adapter.validate({"operations": [{"gate": "h", "qubit": 0}]})
    assert result["backend_id"] == "qiskit"
    assert result["accepted"] is True


def test_benchmark_requires_uncertainty_and_resources() -> None:
    summary = aggregate([
        BenchmarkResult("b1", 0.9, 0.8, 0.01, 10, True),
        BenchmarkResult("b2", 0.85, 0.8, 0.02, 12, False),
    ])
    assert summary["count"] == 2.0
    assert summary["total_quantum_resource_units"] == 22


def test_self_healing_is_bounded_and_non_executing() -> None:
    proposal = propose_remediation("source-x", TimeoutError("timeout"), retryable=True)
    assert proposal.action == RemediationAction.RETRY
    assert proposal.automated is False
    assert proposal.created_at.tzinfo == timezone.utc


def test_capability_discovery_is_safe_without_optional_installs() -> None:
    result = discover_capabilities()
    assert "adapters" in result
    assert result["available_count"] >= 0
