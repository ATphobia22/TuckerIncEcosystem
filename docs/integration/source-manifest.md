# TuckerInc.82 — Cross-Project Source Manifest

## Import policy

This repository is a standalone implementation. Source repositories are **copied, not merged**: their Git histories, branches, remotes, and `.git` directories are not imported.

Only reusable, non-medical assets are candidates for integration. Secrets, credentials, private keys, generated artifacts, caches, vendored dependencies, and unrelated upstream source trees are excluded.

## Verified source corpus

| Source repository | Role | Integration decision |
|---|---|---|
| `ATphobia22/TMRDS` | production data/API/worker patterns | Copy generic infrastructure only; medical/clinical code stays in TMRDS |
| `ATphobia22/tucker_console` | AI comparison, audit logging, console utility | Copy/adapt non-secret audit and orchestration patterns |
| `ATphobia22/Quantum-Studio-1.0` | quantum UI/service patterns | Copy reusable UI/service contracts into isolated quantum namespace |
| `ATphobia22/TuckerB2B` | business/platform workflows | Inspect and copy generic platform utilities only |
| `ATphobia22/vibe-coding-platform` | developer workflow/platform patterns | Inspect and copy reusable developer tooling only |
| `ATphobia22/Python` | Python algorithms/utilities | Use selectively; do not vendor the entire upstream-style tree |
| `ATphobia22/Cortona-Live-Visual-Storytelling-Agent` | multimodal/agent visualization | Copy generic visualization/orchestration patterns only |
| `ATphobia22/CortanaIntelligenceSuiteWorkshopManual` | AI/data engineering reference | Reference/documentation patterns only |
| `ATphobia22/godfirst-llm-ml-protocol` | model protocol patterns | Inspect for generic AI interface contracts |
| `ATphobia22/ai` | AI framework/model utilities | Inspect and isolate reusable non-clinical components |
| `ATphobia22/onyx` | application/AI platform | Inspect for reusable platform patterns |
| `ATphobia22/hermes-agent` | agent runtime patterns | Inspect for bounded agent orchestration |
| `ATphobia22/DeepTutor` | AI/RAG patterns | Inspect for generic retrieval/evaluation patterns |
| `ATphobia22/NextChat` | chat UI/application patterns | Inspect for generic UI contracts |
| `ATphobia22/LMStudio-MCP` | local model/MCP integration | Inspect for local AI connector patterns |
| `ATphobia22/opencode-lmstudio` | coding/model integration | Inspect for developer tooling patterns |
| `ATphobia22/graphify` | graph utilities | Candidate for provenance/dependency graph primitives |
| `ATphobia22/langfuse` | observability/tracing reference | Use patterns only; do not vendor upstream |
| `ATphobia22/openmetadata` | metadata/catalog reference | Use architecture patterns for source/data cataloging |
| `ATphobia22/awesome-osint` | source discovery reference | Reference only; no uncontrolled bulk import |
| `ATphobia22/awesome-scalability` | scalability reference | Reference only |
| `ATphobia22/awesome-cursorrules` | developer rules/reference | Reference only |
| `ATphobia22/everything-claude-code` | coding workflow reference | Reference only |
| `ATphobia22/terminal` | terminal tooling | Inspect for reusable terminal utility patterns |
| `ATphobia22/ghostty` | terminal reference | Reference only unless a bounded utility is required |
| `ATphobia22/TscanCode` | static-analysis tooling | Candidate security/code-quality utility reference |
| `ATphobia22/ultralytics` | computer vision reference | Use bounded inference interfaces only; no model blobs |
| `ATphobia22/ai-hub-models` | model catalog reference | Catalog/reference only; no model weights |
| `ATphobia22/Edge-AI-Model-Zoo` | edge model catalog | Catalog/reference only |
| `ATphobia22/executorch` | edge inference reference | Candidate for future edge inference adapters |
| `ATphobia22/ColossalAI` | distributed AI reference | Reference only unless a bounded component is justified |
| `ATphobia22/qiskit` | quantum computing reference | Reference/integration adapter only; no upstream vendor tree |
| `ATphobia22/cuda-quantum` | quantum computing reference | Reference/integration adapter only |
| `ATphobia22/amazon-braket-sdk-python` | quantum SDK reference | Adapter/reference only |
| `ATphobia22/amazon-braket-default-simulator-python` | quantum simulator reference | Adapter/reference only |
| `ATphobia22/amazon-braket-schemas-python` | quantum schema reference | Candidate for schema interoperability |
| `ATphobia22/classiq-library` | quantum reference | Reference only |
| `ATphobia22/SwiftPixelUtils` | image utilities | Candidate for bounded image processing utilities |
| `ATphobia22/ImageOptim` | image optimization | Candidate for static asset optimization |
| `ATphobia22/jsroot` | scientific visualization | Candidate for scientific-data visualization adapter |
| `ATphobia22/Cactus` | software utility reference | Inspect selectively |
| `ATphobia22/Inscription` | software utility reference | Inspect selectively |
| `ATphobia22/shortid` | identifier utility reference | Prefer native Python UUID/ULID implementation |
| `ATphobia22/awesome-uses` | tooling/reference | Reference only |
| `ATphobia22/build-your-own-x` | engineering reference | Reference only |
| `ATphobia22/starter-workflows` | CI reference | Adapt selected workflow practices |
| `ATphobia22/github-mcp-server` | GitHub integration reference | Reference only; target uses connected GitHub tooling |

## Project-file sources incorporated as structured inputs

- `47620_Grant_Master_Matrix.pdf` — planning baseline for grant intelligence.
- `47620_Grant_link Matrix .pdf` — official-source directory/planning crosswalk.
- `Tri-State Systems Manager Full Production Engine.pdf` — digital-twin/UI and resilience-engineering source material.
- `Tucker Power Implementation Specification.pdf` — power-system, AI governance, cybersecurity, and hydro-development source material.
- `Mount Vernon website.txt` — authoritative municipal website seed URL.

The grant documents explicitly require direct validation against active notices before actionable use. The power specification also establishes an important safety boundary: AI may forecast, detect anomalies, prioritize inspections, and optimize schedules, but it must not independently operate safety-critical power controls or fabricate evidence.

## Explicit exclusions

1. Medical/clinical implementation and patient data.
2. Private keys, tokens, passwords, certificates, and credentials.
3. `.git` directories and source repository history.
4. Large upstream/vendor trees that do not provide a bounded reusable component.
5. Model weights and generated artifacts.
6. Unverified engineering/legal claims presented as authoritative facts.
