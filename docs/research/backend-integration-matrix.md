# Tucker AI Backend Integration Matrix

| Ecosystem | Role in Tucker AI | Integration mode | Base install | Evidence required |
|---|---|---|---|---|
| PennyLane | differentiable QML / hybrid autodiff | optional adapter | no | backend/version + circuit + seed |
| Qiskit Machine Learning | QNNs / quantum kernels / PyTorch hybrid | optional adapter | no | backend/version + kernel/QNN configuration |
| TorchQuantum | PyTorch-native dynamic QNN research | optional adapter | no | torch version + circuit + seed |
| CUDA-Q | CPU/GPU/QPU heterogeneous execution | optional adapter | no | target + hardware/simulator + resource counts |
| Cirq | circuit construction and simulation | optional adapter | no | simulator/version + circuit |
| TensorFlow Quantum | TensorFlow/Keras hybrid QML | optional adapter | no | TF/TFQ/Cirq versions + circuit |
| Mitiq | error mitigation and noisy benchmarks | optional adapter | no | noise model + mitigation method + uncertainty |
| Amazon Braket SDK | managed quantum device execution | optional provider adapter | no | device ARN/name + task ID + shots |
| MerLin | photonic hybrid QML | optional adapter | no | photonic backend + mode/photon configuration |

Tucker AI does not vendor these projects. Their APIs remain external dependencies behind capability adapters. This prevents incompatible licenses, dependency lock-in, and accidental divergence from upstream implementations.

## Current implementation status

The base repository currently implements the provider-neutral contract, deterministic reference simulator, backend capability discovery, governance guardrails, and experiment provenance. Provider execution adapters are intentionally optional and must not be treated as installed merely because they are registered.

## Selection principle

Prefer the smallest backend that can answer the research question. Do not select a quantum backend simply because it is available. Every experiment should state why a quantum component is necessary, what classical baseline is being compared, and what resource constraint is being evaluated.
