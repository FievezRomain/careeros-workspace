# ADR 0004: V1 backend runtime and platform dependencies

- Status: accepted for V1
- Date: 2026-11-22

## Context

CareerOS needs one reproducible backend baseline before service scaffolding begins. The existing decisions already select PostgreSQL and Keycloak, but the backend runtime, asynchronous broker and local S3-compatible implementation were not fixed. Leaving those choices open would make service templates, local infrastructure, contract tests and operational guidance diverge.

The V1 workload is a set of independently deployable services with modest throughput, durable workflow events, binary resume artifacts, strict authorization boundaries and no requirement for internet-scale streaming.

## Decision

### Backend runtime

Backend services use Node.js 26 LTS and TypeScript in strict mode. Each repository pins the Node.js major and a current security patch in its development, CI and container configuration. A service may use a different runtime only through a new ADR that explains the operational and contract impact.

Shared code is limited to versioned contract packages and narrowly scoped tooling. Services remain independently buildable and deployable; a shared runtime does not permit shared databases or a distributed monolith.

### Persistence isolation

Business services use PostgreSQL 16 as defined by [ADR 0002](0002-postgresql-default-persistence.md). Every service owns a separate logical database, role, credentials and migration history. One PostgreSQL cluster may host several databases in local development, but cross-database queries, shared schemas and reused service credentials are prohibited.

Keycloak owns a separate database and credentials. No business service reads Keycloak tables.

### Asynchronous broker

RabbitMQ 4.x over AMQP 0-9-1 is the V1 broker for durable domain events and background work. Synchronous queries and immediate commands remain versioned HTTP APIs; the broker is not a substitute for service APIs.

Durable production flows use quorum queues, persistent messages, publisher confirms and manual consumer acknowledgements. Retry limits and dead-letter routing are explicit. Delivery is at least once, so consumers must be idempotent and deduplicate using stable message identifiers. Event payloads are minimized and carry references instead of raw resumes, applications or other large sensitive content. Event naming, envelopes and compatibility rules are defined by V1-003.

The local single-node broker preserves the same exchanges, queues and policies but does not claim production availability.

### Object storage

Services access binary artifacts through the supported Amazon S3 API subset rather than a provider-specific SDK surface. The local Compose baseline uses a pinned SeaweedFS release with its S3 gateway. Production may use another maintained S3-compatible provider when the same storage contract tests pass.

The owning service keeps artifact metadata, provenance, checksums and immutable object references in its PostgreSQL database. Buckets and credentials are scoped by owning service. Object keys are opaque, provider credentials come from environment-specific secret stores, and short-lived download URLs are issued only after authorization and ownership checks. Retention and deletion are driven by owning-service policy.

### Identity provider

Keycloak remains the V1 identity provider as defined by [ADR 0003](0003-keycloak-identity-provider.md). Services depend on configured OpenID Connect issuer, audience and claims, not on the physical Keycloak deployment. Every service validates token integrity and authorization context at its own boundary; network placement alone is never authorization.

## Consequences

- Service scaffolds can share one supported language toolchain while retaining independent releases and ownership.
- PostgreSQL and object storage have distinct responsibilities: relational state and artifact metadata stay transactional, while binary content stays outside database columns.
- RabbitMQ provides durable routing, acknowledgements and dead-letter handling without introducing the operational footprint of a streaming platform that V1 does not need.
- At-least-once delivery makes idempotency and replay tests mandatory for consumers; CareerOS does not claim exactly-once processing.
- The local object store is replaceable because applications target a tested S3 subset rather than SeaweedFS-specific APIs.
- Production deployments still need environment-specific high availability, capacity, encryption, backup, restore and monitoring decisions.

## Rejected alternatives

- Kafka is not selected because V1 does not require long-lived high-throughput event streams or replay at that operational cost.
- An in-process queue or database polling is not selected because it couples services and weakens independent delivery and failure isolation.
- Provider-specific object-storage APIs are not selected because they would prevent reproducible local development and make provider changes invasive.
- Unmaintained prebuilt MinIO community releases are not selected for the local baseline. The storage contract remains S3-compatible so the implementation can change independently.
- A shared PostgreSQL database with per-service schemas is not selected because credentials or queries could cross service ownership boundaries.

## Delivery impact

- V1-003 defines the API and event compatibility conventions used above.
- V1-004 implements PostgreSQL databases, RabbitMQ and SeaweedFS in the local Compose stack with placeholder configuration.
- V1-007 turns the runtime, isolation, health, migration and test requirements into an executable service checklist.
- V1-046 verifies backup and restore for service-owned data and artifact metadata.

No public API or event contract changes in this ADR. Future changes to the selected runtime or platform dependencies require a superseding ADR and an explicit migration plan.

## References

- [Node.js release schedule](https://nodejs.org/en/about/previous-releases)
- [PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/)
- [RabbitMQ quorum queues](https://www.rabbitmq.com/docs/quorum-queues)
- [SeaweedFS project and S3 gateway](https://github.com/seaweedfs/seaweedfs)
- [Keycloak documentation](https://www.keycloak.org/documentation)
