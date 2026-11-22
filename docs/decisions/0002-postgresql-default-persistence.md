# ADR 0002: PostgreSQL as the V1 business datastore

- Status: proposed for V1
- Date: 2026-11-22

## Context

CareerOS manages profiles, evidence, opportunity versions, application state transitions, approvals and audit references. These records have explicit relationships and invariants. Some source payloads are semi-structured, while resumes and generated documents are binary artifacts.

## Decision

Use PostgreSQL as the default system of record for V1 services. Each service owns an isolated database or database namespace and dedicated credentials. Services never query another service's tables. Use JSONB only for values whose structure is genuinely variable, such as preserved source payloads and provider metadata.

Store PDF/DOCX artifacts in S3-compatible object storage and keep only their metadata and immutable references in the owning service. Add vector search only when a measured use case justifies it; it is not a prerequisite for deterministic V1 matching.

## Consequences

- Transactions, constraints, migrations and reporting semantics remain explicit.
- Semi-structured input does not force the whole model into unvalidated documents.
- Cross-service behavior uses versioned public contracts rather than shared joins.
- MongoDB may still be chosen later for a bounded, document-centric use case through a new ADR; it is not the default.
