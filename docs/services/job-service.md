# careeros-job-service

Normalized opportunities, source provenance, deduplication and freshness.

Repository: https://github.com/FievezRomain/careeros-job-service

## V1 runtime boundary

- Python 3.14 with Pydantic v2 boundary and configuration models.
- Inward-facing hexagonal dependencies: application startup owns the migration port; SQLAlchemy remains in the PostgreSQL adapter.
- The composition root injects the PostgreSQL migration runner into the startup use case.
- PostgreSQL 16 is service-owned. No other service may read its database, role, schema or migration ledger.
- Migration scripts and runner live under `adapters/postgresql/migrations`. Startup applies pending revisions, verifies every expected head and fails before serving traffic on mismatch.
- `/health/live` and `/health/ready` remain operational endpoints only.
- `POST /v1/jobs/manual` implements `BR-JOB-001` and `BR-JOB-002`. It requires an authenticated account, the `jobs:write` scope and an idempotency key.
- Ownership and tenant identifiers come only from the verified identity context. The request cannot select them.
- Manual capture preserves the submitted title, employer, description, source reference and exact raw source wording, with a server-recorded capture time.
- Replaying the same command returns the original opportunity; reusing its key for different content is rejected.
- `BR-JOB-003`, `BR-JOB-004` and `BR-JOB-006` govern the normalized catalog delivered by V1-019.
- User-visible title, employer and description text is normalized deterministically with Unicode NFKC and collapsed whitespace while source wording remains unchanged for provenance.
- Equivalent normalized title and employer identities share a group. Repeated material content is deduplicated, changed content creates a new immutable version and `forceSeparate` starts a distinct group when automatic grouping is wrong.
- `GET /v1/jobs?page=<n>&pageSize=<n>` returns the authenticated owner's latest version per group; `GET /v1/jobs/{opportunityId}` returns one owned immutable version. Both require `jobs:read`, and missing or differently owned identifiers return not found.
- Catalog responses identify source-stated fields and keep inferred and unknown information distinguishable.
- `POST /v1/internal/discovery/search-snapshots` consumes the versioned
  `profile.match-relevant-change.v1` projection. It requires the internal
  `discovery:write` scope and ignores duplicate or older projections.
- `POST /v1/internal/discovery/runs` requires `discovery:run`, a correlation
  identifier and an idempotency key. It selects active searches in their own
  IANA-timezone window, runs each search at most once per local day and shares
  retrieval only between identical search signatures.
- Daily discovery is orchestrated by application-owned ports for search
  projections, source collection, observations, checkpoints and outbox events.
  SQLAlchemy, PostgreSQL and HTTP provider details remain in adapters and are
  injected by the composition root.
- The first structured-source adapter uses Greenhouse's public Job Board API.
  It retrieves the configured board in full, retains conditional-request and
  rate-limit evidence, and reports truncation instead of silently discarding
  results. Generic or authenticated scraping and protection bypass are excluded.
- An unchanged rediscovery updates `lastSeenAt`; materially changed source
  content creates a new immutable opportunity version and a transactional
  `job.opportunity-version-discovered.v1` outbox event. Failed run claims remain
  retryable and completed commands replay safely.

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.

The service stores owned opportunity versions, capture-command idempotency and source provenance. It stores no resume, application or contact data and exposes no cross-owner records.

Automatically discovered records retain the source URL, external identifier,
exact source wording and first/last observation times for audit. These payloads
are never logged.
