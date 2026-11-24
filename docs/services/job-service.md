# careeros-job-service

Normalized opportunities, source provenance, deduplication and freshness.

Repository: https://github.com/FievezRomain/careeros-job-service

## V1 runtime boundary

- Python 3.14 with Pydantic v2 boundary and configuration models.
- Inward-facing hexagonal dependencies: application startup owns the migration port; SQLAlchemy remains in the PostgreSQL adapter.
- The composition root injects the PostgreSQL migration runner into the startup use case.
- PostgreSQL 16 is service-owned. No other service may read its database, role, schema or migration ledger.
- Migration scripts and runner live under `adapters/postgresql/migrations`. Startup applies pending revisions, verifies every expected head and fails before serving traffic on mismatch.
- The scaffold exposes liveness and readiness only. Manual capture, provenance, normalization and query behavior remain scoped to V1-018 and V1-019.

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.

The initial schema contains only opaque job and owner identifiers plus timestamps. It intentionally stores no raw source payload, resume, application or contact data.
