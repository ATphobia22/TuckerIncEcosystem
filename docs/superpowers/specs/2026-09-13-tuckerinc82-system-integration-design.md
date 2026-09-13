# TuckerInc.82 — Standalone Cross-Project Integration & Real-Time Data Fabric Design

## Status
Approved architecture; implementation gated on spec review.

## Objective
Transform `ATphobia22/TuckerInc.82` into a clean, production-grade standalone system that **copies reusable assets** from the user's available project/repository corpus without merging repository histories, while adding a shared real-world/current-data fabric and preserving strict domain boundaries.

## Source policy
- Source repositories remain untouched.
- Copy reusable source code, validated components, schemas/contracts, tests, tooling, documentation, configuration patterns, and data-source definitions only after inspection.
- Do not copy `.git` histories, credentials, tokens, private keys, caches, generated build artifacts, vendored dependencies, or knowingly broken/obsolete code.
- Every copied component receives provenance metadata: source repository, source path, source revision/commit when available, destination path, license/usage note when available, and rationale.
- Existing `TuckerInc.82` content is retained unless it is replaced by a verified production implementation or is explicitly classified as obsolete.

## Domain boundary
Medical/clinical implementation is excluded from TuckerInc.82. Medical systems and clinical code remain in TMRDS. Non-medical reusable infrastructure (generic data fabric, observability, geospatial primitives, developer tooling, security patterns, etc.) may be copied when it contains no clinical functionality or patient data.

## Target architecture
```text
External authoritative sources
        |
        v
Source Registry / Scheduler
        |
        v
Ingestion adapters -> Raw evidence store
        |                     |
        v                     v
Validation -------------> Provenance ledger
        |
        v
Normalization / canonical contracts
        |
        +--> Freshness / quality state
        |
        v
Current-state store + event stream
        |
        +--> REST API / health / metrics
        +--> grant intelligence
        +--> geospatial / hydrology
        +--> engineering / simulation adapters
        +--> applications and utilities
```

## Core components
### 1. Repository integration layer
A manifest-driven importer copies approved assets into bounded namespaces such as `apps/`, `packages/`, `services/`, `data/`, `infrastructure/`, `docs/`, and `tests/`. Namespaces prevent accidental cross-domain coupling.

### 2. Data fabric
Canonical records must retain source identity, canonical source URL/API, retrieval time, source timestamp when supplied, cadence, schema version, geographic scope, CRS/datum when applicable, validation state, freshness state, content hash, and transformation lineage.

Real-time semantics are explicit: `realtime`, `near_realtime`, `daily`, `periodic`, `event_driven`, or `static_reference`. A periodic publisher is never represented as real-time merely because the platform polls it frequently.

### 3. Evidence and provenance
Raw source payloads are immutable evidence objects. Derived records reference their source evidence and transformation chain. Hashes are used for integrity; timestamps use UTC; provenance identifiers are stable and machine-readable.

### 4. Validation
Adapters validate transport status, payload shape, required fields, units, timestamps, geographic validity, CRS metadata, and domain-specific constraints. Invalid or stale data is retained with an explicit status rather than silently substituted with synthetic values.

### 5. Grant intelligence
The 47620 grant matrix is represented as source-audited structured data, with official-source registry, opportunity status, applicant eligibility, award/match fields, deadlines, project crosswalks, and evidence references. Current status must be revalidated against authoritative sources before being presented as actionable.

### 6. Geospatial / resilience fabric
Support WGS84 and authoritative project CRSs explicitly; retain horizontal/vertical datum metadata; provide spatial feature contracts suitable for flood, terrain, infrastructure, and planning datasets. Existing engineering calculation authority remains separate from visualization.

### 7. Applications and utilities
Existing useful utilities are copied into isolated modules and adapted behind stable interfaces. Utilities must not contain hidden network credentials or domain-specific medical behavior.

### 8. Observability and operations
Add structured logging, health/readiness endpoints, source-level ingestion metrics, freshness metrics, failure counters, trace/provenance IDs, configuration validation, and deterministic test fixtures. CI must run formatting/static checks/tests/build checks appropriate to each component.

## Current verified grant/source baseline
The project files establish a 47620 strategic funding framework spanning federal grant infrastructure; FEMA/emergency management; USACE/NOAA; EPA/IDEM/IFA; HUD/OCRA/IHCDA; USDA Rural Development; transportation/ports; broadband/digital infrastructure; economic development; workforce/education; DOJ/public safety; health/rural health; energy; agriculture/food systems; nonprofit/faith-based pathways; and private/foundation funding. The attached master matrix explicitly requires direct validation against active federal NOFOs before actionable use.

The grant fabric will therefore store the matrix as a **planning baseline**, not as an immutable statement of current eligibility/deadlines. The live source registry is authoritative for current state.

## Security requirements
- Never copy secrets or credentials.
- Secrets come from environment/configuration injection, never source control.
- Validate and constrain outbound URLs and source adapters.
- Apply timeouts, bounded payload sizes, retry/backoff, and circuit-breaker behavior to external ingestion.
- Treat external payloads as untrusted input.
- Keep raw evidence immutable and derived state reproducible.
- No fabricated compliance, legal, medical, or engineering certifications.

## Testing strategy
- Contract tests for every source adapter.
- Unit tests for normalization, validation, freshness, hashing, provenance, and CRS metadata.
- Integration tests for ingestion-to-current-state flow.
- Regression tests for copied utilities.
- API smoke tests and health/readiness tests.
- Static analysis and dependency/security checks.
- Deterministic fixtures for external-source failures and malformed payloads.

## Acceptance criteria
1. TuckerInc.82 contains no copied Git history from source repositories.
2. A machine-readable source manifest identifies copied assets and provenance.
3. Medical/clinical implementation is absent from the target integration.
4. The data fabric can ingest, validate, normalize, fingerprint, and expose current state with explicit freshness semantics.
5. Raw evidence and provenance are retained for auditability.
6. Grant intelligence is structured and traceable to source records.
7. Existing useful utilities are isolated behind stable interfaces.
8. Secrets and generated artifacts are excluded.
9. CI/tests/build checks pass for the integrated system.
10. README and operational documentation accurately describe what is implemented versus merely planned.

## Initial source families to inspect
The project corpus indicates relevant work across TMRDS, Tri-State/Tri-County engineering systems, PTDT, Python/open-source data tooling, quantum/software tooling, Tucker Console/SGE, B2B/platform utilities, visualization/VFX tooling, and other ATphobia22 repositories. The full GitHub inventory must be enumerated and classified before copying; filenames or prior summaries are not treated as proof of repository contents.
