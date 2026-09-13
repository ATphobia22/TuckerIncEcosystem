# Tucker AI Quantum Machine Learning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a provider-neutral Tucker AI hybrid quantum-classical research layer with ethical guardrails, reproducible experiments, and optional integrations with major quantum ML ecosystems.

**Architecture:** Keep the base runtime dependency-light and deterministic. Use a native small-circuit reference backend for tests and research baselines, then expose optional adapters for PennyLane, Qiskit ML, TorchQuantum, CUDA-Q, Cirq/TFQ, Mitiq, Braket, and MerLin. Persist evidence and provenance through the existing data-fabric primitives.

**Tech Stack:** Python, Pydantic, FastAPI, NumPy, optional quantum SDKs, pytest, Ruff, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-13-tucker-ai-qml-design.md`

## Global Constraints

- No medical/clinical implementation; medical work remains in TMRDS.
- No wholesale copying of third-party repositories; implement adapter contracts and preserve third-party license boundaries.
- No secrets or credentials in source control.
- External source retrieval must remain HTTPS and exact-allowlisted.
- Quantum advantage claims require reproducible classical baselines and measured evidence.
- Guardrail outcomes are `allow`, `review`, or `deny`; ambiguity defaults to `review`.
- All experiment artifacts must carry deterministic configuration and integrity metadata.

---

### Task 1: Harden source ingestion

**Files:**
- Modify: `tuckerinc82/registry.py`
- Modify: `tuckerinc82/ingestion.py`
- Test: `tests/test_ingestion_security.py`

- [ ] Add exact registered-endpoint validation.
- [ ] Reject redirects whose final destination is not the registered HTTPS endpoint.
- [ ] Add tests for same-host wrong-path rejection and redirect rejection.
- [ ] Run `pytest tests/test_ingestion_security.py -v`.
- [ ] Commit `security: harden authoritative source ingestion`.

### Task 2: Implement God is Love Protocol guardrails

**Files:**
- Create: `tuckerinc82/guardrails.py`
- Test: `tests/test_guardrails.py`

- [ ] Define typed principles and decision levels.
- [ ] Implement deterministic policy evaluation for dignity, non-maleficence, truthfulness, consent, privacy, fairness, transparency, accountability, and human oversight.
- [ ] Default ambiguous/high-impact actions to `review`.
- [ ] Add tests for allow/review/deny behavior.
- [ ] Run `pytest tests/test_guardrails.py -v`.
- [ ] Commit `feat: add Tucker AI ethical guardrails`.

### Task 3: Implement Tucker AI experiment contracts

**Files:**
- Create: `tuckerinc82/tucker_ai.py`
- Create: `tuckerinc82/quantum_reference.py`
- Test: `tests/test_tucker_ai.py`

- [ ] Define circuit/model/experiment Pydantic contracts.
- [ ] Implement a deterministic small statevector reference backend using NumPy.
- [ ] Implement angle encoding, parameterized single-qubit rotations, entangling CNOTs, expectation measurement, and reproducible seeds.
- [ ] Implement a minimal hybrid VQC execution contract with classical preprocessing/postprocessing represented explicitly.
- [ ] Add integrity hashes and provenance identifiers to experiment results.
- [ ] Test deterministic repeated execution and malformed circuit rejection.
- [ ] Run `pytest tests/test_tucker_ai.py -v`.
- [ ] Commit `feat: add Tucker AI hybrid quantum core`.

### Task 4: Add backend capability registry

**Files:**
- Create: `tuckerinc82/backends.py`
- Create: `data/quantum/backend_registry.json`
- Test: `tests/test_backends.py`

- [ ] Register PennyLane, Qiskit ML, TorchQuantum, CUDA-Q, Cirq/TFQ, Braket, Mitiq, and MerLin as optional capabilities.
- [ ] Implement import-safe capability discovery using `importlib.util.find_spec`.
- [ ] Never import optional providers during base-module import.
- [ ] Test discovery behavior without requiring provider installations.
- [ ] Commit `feat: add optional quantum backend registry`.

### Task 5: Add API surface

**Files:**
- Modify: `tuckerinc82/app.py`
- Test: `tests/test_app.py`

- [ ] Add `/api/tucker-ai/capabilities`.
- [ ] Add `/api/tucker-ai/guardrails/evaluate`.
- [ ] Add `/api/tucker-ai/experiments/validate`.
- [ ] Keep API responses typed and deterministic.
- [ ] Run the full application test suite.
- [ ] Commit `feat: expose Tucker AI API contracts`.

### Task 6: Add benchmark and research governance

**Files:**
- Create: `docs/research/tucker-ai-benchmark-protocol.md`
- Create: `docs/research/backend-integration-matrix.md`
- Create: `tests/test_research_contracts.py`

- [ ] Specify classical baseline, hybrid model, noisy model, mitigation model, seed policy, confidence intervals, resource accounting, and simulator/QPU distinction.
- [ ] Record that current implementation makes no quantum-advantage claim.
- [ ] Document licensing and adapter isolation.
- [ ] Commit `docs: establish Tucker AI research benchmark protocol`.

### Task 7: Verify and integrate

**Files:**
- Modify: `README.md`
- Modify: `pyproject.toml`
- Modify: `.github/workflows/ci.yml`

- [ ] Add optional dependency groups without forcing heavyweight quantum SDKs into the base runtime.
- [ ] Add NumPy as the reference-backend dependency.
- [ ] Test supported Python versions in CI.
- [ ] Run `pytest -q` and `ruff check .`.
- [ ] Inspect Git diff and repository tree for secrets, generated artifacts, and unintended vendoring.
- [ ] Commit `feat: integrate Tucker AI research platform`.

## Final verification

Run the complete test suite, linting, import checks, and the GitHub Actions workflow. Do not claim production readiness until the resulting checks are green. A passing local test suite does not constitute quantum advantage or regulatory certification.
