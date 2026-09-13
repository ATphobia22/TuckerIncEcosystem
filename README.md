# TuckerInc.82 — Tucker AI

Standalone production foundation for **Tucker AI**: hybrid quantum-classical AI research, authoritative real-world data fabric, geospatial/resilience tooling, grant intelligence, and reusable software utilities.

## Architecture

```text
Authoritative Sources
        ↓
Source Registry → Bounded Ingestion → Immutable Evidence
        ↓                         ↓
Validation → Normalization → Provenance
        ↓
Freshness / Quality State
        ↓
Tucker AI Governance → Hybrid Quantum/Classical Execution
        ↓
Research Benchmarks / Applications / Analytics
```

## Tucker AI

The repository provides a provider-neutral quantum-AI layer with:

- deterministic small-circuit statevector reference execution;
- typed hybrid experiment contracts;
- reproducibility hashes and provenance identifiers;
- machine-checkable **God is Love Protocol** guardrails with `allow`, `review`, and `deny` outcomes;
- optional capability discovery for PennyLane, Qiskit Machine Learning, TorchQuantum, CUDA-Q, Cirq, TensorFlow Quantum, Mitiq, Amazon Braket, and MerLin;
- a research registry covering major open quantum/QML stacks and interoperability standards;
- an explicit benchmark protocol requiring classical baselines, uncertainty, resource accounting, and simulator/QPU separation;
- no unsupported quantum-advantage claims.

The backend ecosystem is adapter-based rather than wholesale vendored. This keeps upstream licenses, release cadence, and dependency boundaries intact.

## Deep quantum-AI research

The current framework survey, architecture recommendations, standards mapping, and innovation roadmap are documented in:

- `docs/quantum/tucker-ai-research.md`
- `data/quantum/framework_registry.json`
- `docs/research/backend-integration-matrix.md`
- `docs/research/tucker-ai-benchmark-protocol.md`
- `docs/superpowers/specs/2026-09-13-tucker-ai-qml-design.md`
- `docs/superpowers/plans/2026-09-13-tucker-ai-qml.md`

The interoperability strategy uses **OpenQASM 3** and **QIR** as standards-oriented boundaries where practical. Responsible-AI governance is aligned conceptually with NIST AI RMF, ISO/IEC 42001, and UNESCO's AI ethics recommendation; Tucker AI does not claim certification under any of them.

## Current implementation

- FastAPI gateway with health, source registry, Tucker AI capability, guardrail, and experiment-validation endpoints.
- Strict Pydantic data contracts with UTC timestamp validation.
- Deterministic SHA-256 content fingerprints.
- Explicit current/stale/expired freshness semantics.
- Exact HTTPS endpoint allowlists and redirect validation for JSON ingestion.
- Bounded external payload size and request timeout.
- Content-addressed raw evidence store.
- Provenance event contract.
- Explicit horizontal CRS / vertical datum metadata contract.
- 47620 grant-intelligence planning baseline with live-source revalidation policy.
- Cross-project source manifest documenting copied/adapted assets.
- Preserved Tucker Console compatibility utility under `legacy/`.
- GitHub Actions CI for Ruff and Pytest.

## Dependency strategy

The base runtime stays lightweight. Heavy quantum stacks are optional extras so a clean deployment does not inherit every vendor/runtime dependency.

```bash
python -m pip install -e '.[dev]'
python -m pip install -e '.[qml]'
python -m pip install -e '.[photonic]'
python -m pip install -e '.[physics]'
python -m pip install -e '.[optimization]'
python -m pip install -e '.[tensorflow-quantum]'
```

Provider availability and platform compatibility must be verified before a production deployment. Optional extras are not a promise that every framework can coexist in one Python environment.

## Source integration policy

Source repositories are copied selectively into bounded namespaces; repository histories are never merged into this project. Source repositories remain independent. External frameworks are integrated through documented contracts and optional adapters rather than copied wholesale.

The integration manifest is at `docs/integration/source-manifest.md`.

## Domain boundary

Medical and clinical implementation is intentionally excluded. Medical systems remain in TMRDS. TuckerInc.82 may contain generic infrastructure only when it has no patient/clinical functionality or data.

## Data authority

Project documents are planning inputs. Current grant status, deadlines, eligibility, regulatory requirements, engineering facts, and external measurements must be revalidated against the registered authoritative source before operational use.

## Development

```bash
python -m pip install -e '.[dev]'
ruff check .
pytest -q
```

Application entrypoint: `main:app`.

## Security baseline

Do not commit API keys, tokens, private keys, certificates, credentials, model weights, generated artifacts, or `.env` files. External data is untrusted input and must pass transport, schema, size, timestamp, and provenance controls before becoming current state.

## Ethical governance

The God is Love Protocol is a user-authored governance layer emphasizing human dignity, non-maleficence, truthfulness, consent, privacy, fairness, transparency, accountability, and human oversight. It is not presented as legal, regulatory, scientific, or religious certification and does not override applicable law, safety controls, or legitimate human governance.
