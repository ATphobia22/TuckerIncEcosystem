# Tucker AI interoperability architecture

## Verified upstreams

The quantum adapter registry is intentionally provider-neutral. Current source verification includes Qiskit, Cirq, Microsoft QDK, Quantinuum TKET, D-Wave Ocean, Rigetti PyQuil, Pasqal Pulser, PsiQuantum Bartiq, and Q-CTRL Open Controls. Each remains an external dependency; Tucker AI does not vendor or merge upstream histories.

## Evidence and events

1. `source_mesh.py` validates HTTPS authoritative endpoints and exposes only enabled sources.
2. `evidence.py` writes immutable content-addressed evidence under `data/evidence/<source>/<sha256>.json`.
3. `event_bus.py` provides bounded in-process dispatch, event-id deduplication, and a replayable dead-letter queue.
4. `repository_intelligence.py` classifies repository components into bounded architectural categories.

## Quantum interoperability

`quantum_adapters.py` provides a dependency-neutral adapter factory. Optional providers are discovered without importing their SDKs unless an adapter is initialized. `capabilities.py` exposes installed-provider discovery. The benchmark layer requires both quantum and classical baselines, uncertainty, resource accounting, and explicit simulator/QPU state.

## Optional context index

`turbovec_boundary.py` is an isolated optional boundary around TurboVec/TurboQuant. It is never imported by the base runtime unless used. The external project is a Rust/Python vector index; the boundary keeps persistence and retrieval implementation outside the core data contracts.

## Browser AI and WebMCP

`chrome_ai.py` is a capability descriptor rather than a server-side model invocation. Chrome's built-in Prompt API is browser-managed and has platform/hardware availability constraints. The browser client must own model invocation and must not expose secrets.

`webmcp.py` provides governed tool metadata and confirmation policy. `public/webmcp/tucker-tools.js` registers read-only Tucker tools with `document.modelContext` when available. WebMCP is currently an evolving browser draft/preview, not a backend MCP transport; consequential operations remain confirmation-gated.

## Security boundary

External data is untrusted. Tool descriptions and outputs can carry indirect prompt-injection content. Do not treat browser-generated instructions, third-party text, or tool output as trusted policy. All consequential operations require explicit governance outside the model's authority.

## Medical boundary

No medical or clinical implementation is included. Medical systems remain in TMRDS as directed by the project boundary.
