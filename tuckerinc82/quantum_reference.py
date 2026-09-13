from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin

import numpy as np


@dataclass(frozen=True)
class GateOperation:
    name: str
    target: int
    angle: float = 0.0
    control: int | None = None


def _rx(theta: float) -> np.ndarray:
    return np.array(
        [[cos(theta / 2), -1j * sin(theta / 2)], [-1j * sin(theta / 2), cos(theta / 2)]],
        dtype=complex,
    )


def _ry(theta: float) -> np.ndarray:
    return np.array(
        [[cos(theta / 2), -sin(theta / 2)], [sin(theta / 2), cos(theta / 2)]],
        dtype=complex,
    )


def _rz(theta: float) -> np.ndarray:
    return np.array(
        [[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]],
        dtype=complex,
    )


def _apply_single_qubit(state: np.ndarray, matrix: np.ndarray, target: int, n_qubits: int) -> np.ndarray:
    reshaped = state.reshape([2] * n_qubits)
    axes = [target] + [index for index in range(n_qubits) if index != target]
    moved = np.transpose(reshaped, axes).reshape(2, -1)
    updated = matrix @ moved
    inverse_axes = np.argsort(axes)
    return np.transpose(updated.reshape([2] * n_qubits), inverse_axes).reshape(-1)


def _apply_cnot(state: np.ndarray, control: int, target: int, n_qubits: int) -> np.ndarray:
    updated = state.copy()
    for index in range(len(state)):
        control_bit = (index >> (n_qubits - control - 1)) & 1
        target_bit = (index >> (n_qubits - target - 1)) & 1
        if control_bit == 1 and target_bit == 0:
            partner = index | (1 << (n_qubits - target - 1))
            updated[index], updated[partner] = state[partner], state[index]
    return updated


def simulate_statevector(n_qubits: int, operations: list[GateOperation]) -> np.ndarray:
    if n_qubits < 1 or n_qubits > 12:
        raise ValueError("reference simulator supports between 1 and 12 qubits")
    state = np.zeros(2**n_qubits, dtype=complex)
    state[0] = 1.0
    for operation in operations:
        if operation.target < 0 or operation.target >= n_qubits:
            raise ValueError("gate target is outside the circuit")
        if operation.name == "rx":
            state = _apply_single_qubit(state, _rx(operation.angle), operation.target, n_qubits)
        elif operation.name == "ry":
            state = _apply_single_qubit(state, _ry(operation.angle), operation.target, n_qubits)
        elif operation.name == "rz":
            state = _apply_single_qubit(state, _rz(operation.angle), operation.target, n_qubits)
        elif operation.name == "cnot":
            if operation.control is None or operation.control == operation.target:
                raise ValueError("CNOT requires a distinct control qubit")
            if operation.control < 0 or operation.control >= n_qubits:
                raise ValueError("CNOT control is outside the circuit")
            state = _apply_cnot(state, operation.control, operation.target, n_qubits)
        else:
            raise ValueError(f"unsupported reference gate: {operation.name}")
    return state


def expectation_z(state: np.ndarray, target: int, n_qubits: int) -> float:
    if target < 0 or target >= n_qubits:
        raise ValueError("measurement target is outside the circuit")
    expectation = 0.0
    for index, amplitude in enumerate(state):
        bit = (index >> (n_qubits - target - 1)) & 1
        expectation += (1.0 if bit == 0 else -1.0) * float(abs(amplitude) ** 2)
    return float(expectation)
