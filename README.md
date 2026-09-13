# TuckerInc.82

Standalone production foundation for Tucker's cross-project software assets, real-world data fabric, geospatial/resilience tooling, grant intelligence, AI/quantum adapters, and reusable utilities.

## Architecture

```text
Authoritative Sources
        ↓
Source Registry → Bounded Ingestion → Raw Evidence
        ↓                         ↓
Validation → Normalization → Provenance Ledger
        ↓
Freshness / Quality State
        ↓
Current-State API → Applications / Utilities / Analytics
```

## Current implementation

- FastAPI gateway with health and source-registry endpoints.
- Strict Pydantic data contracts with UTC timestamp validation.
- Deterministic SHA-256 content fingerprints.
- Explicit current/stale/expired freshness semantics.
- HTTPS and registered-origin controls for JSON ingestion.
- Bounded external payload size and request timeout.
- Content-addressed raw evidence store.
- Provenance event contract.
- Explicit horizontal CRS / vertical datum metadata contract.
- 47620 grant-intelligence planning baseline with live-source revalidation policy.
- Cross-project source manifest documenting copied/adapted assets.
- Preserved Tucker Console compatibility utility under `legacy/`.
- GitHub Actions CI for Ruff and Pytest.

## Source integration policy

Source repositories are copied selectively into bounded namespaces; repository histories are never merged into this project. Source repositories remain independent.

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
