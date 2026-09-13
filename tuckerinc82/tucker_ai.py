from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Literal

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .guardrails import GuardrailRequest, GuardrailResult, evaluate_guardrails
from .provenance import make_provenance_id
from .quantum_reference import GateOperation, expectation_z, simulate_statevector


class QuantumOperation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Literal["rx", "ry", "rz", "cnot"]
    target: int = Field(ge=0)
    control: int | None = Field(default=None, ge=0)
    angle: float = 0.0


class TuckerQuantumCircuit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    n_qubits: int = Field(ge=1, le=12)
    operations: list[QuantumOperation] = Field(default_factory=list, max_length=512)
    measure_qubit: int = Field(default=0, ge=0)


class TuckerExperiment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_id: str = Field(min_length=1, max_length=128)
    circuit: TuckerQuantumCircuit
    seed: int = Field(default=0, ge=0)
    classical_features: list[float] = Field(default_factory=list, max_length=4096)
    guardrails: GuardrailRequest

    @field_validator("circuit")
    @classmethod
    def validate_measurement(cls, value: TuckerQuantumCircuit) -> TuckerQuantumCircuit:
        if value.measure_qubit >= value.n_qubits:
            raise ValueError("measurement qubit must be within the circuit")
        return value


class TuckerExperimentResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_id: str
    backend: str
    expectation: float
    decision: str
    provenance_id: str
    configuration_hash: str
    executed_at: datetime


def _configuration_hash(experiment: TuckerExperiment) -> str:
    canonical = json.dumps(experiment.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def run_reference_experiment(experiment: TuckerExperiment) -> TuckerExperimentResult:
    guardrail_result: GuardrailResult = evaluate_guardrails(experiment.guardrails)
    if guardrail_result.decision.value != "allow":
        raise PermissionError(f"Tucker AI guardrail decision: {guardrail_result.decision.value}")

    np.random.default_rng(experiment.seed)
    operations = [
        GateOperation(
            name=operation.name,
            target=operation.target,
            control=operation.control,
            angle=operation.angle,
        )
        for operation in experiment.circuit.operations
    ]
    state = simulate_statevector(experiment.circuit.n_qubits, operations)
    expectation = expectation_z(state, experiment.circuit.measure_qubit, experiment.circuit.n_qubits)
    executed_at = datetime.now(timezone.utc)
    config_hash = _configuration_hash(experiment)
    provenance_id = make_provenance_id(
        source_id="tucker-ai-reference",
        input_hash=config_hash,
        output_hash=hashlib.sha256(f"{expectation:.17g}".encode("utf-8")).hexdigest(),
    )
    return TuckerExperimentResult(
        experiment_id=experiment.experiment_id,
        backend="reference-statevector",
        expectation=expectation,
        decision=guardrail_result.decision.value,
        provenance_id=provenance_id,
        configuration_hash=config_hash,
        executed_at=executed_at,
    )
