import pytest

from tuckerinc82.guardrails import GuardrailRequest
from tuckerinc82.tucker_ai import (
    QuantumOperation,
    TuckerExperiment,
    TuckerQuantumCircuit,
    run_reference_experiment,
)


def _experiment() -> TuckerExperiment:
    return TuckerExperiment(
        experiment_id="deterministic-z",
        circuit=TuckerQuantumCircuit(
            n_qubits=1,
            operations=[QuantumOperation(name="ry", target=0, angle=0.0)],
            measure_qubit=0,
        ),
        seed=42,
        guardrails=GuardrailRequest(purpose="unit test", impact_level="low"),
    )


def test_reference_experiment_is_deterministic_except_execution_timestamp():
    first = run_reference_experiment(_experiment())
    second = run_reference_experiment(_experiment())
    assert first.expectation == second.expectation
    assert first.configuration_hash == second.configuration_hash
    assert first.provenance_id == second.provenance_id


def test_guardrail_review_blocks_execution():
    experiment = _experiment().model_copy(
        update={
            "guardrails": GuardrailRequest(
                purpose="high impact",
                impact_level="high",
                has_human_oversight=False,
            )
        }
    )
    with pytest.raises(PermissionError, match="review"):
        run_reference_experiment(experiment)


def test_measurement_qubit_must_exist():
    with pytest.raises(ValueError):
        TuckerQuantumCircuit(n_qubits=1, measure_qubit=1)
