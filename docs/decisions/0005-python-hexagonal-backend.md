# ADR 0005: Python and hexagonal architecture for V1 backend services

- Status: accepted for V1
- Date: 2026-11-22
- Supersedes: the backend runtime section of [ADR 0004](0004-v1-backend-platform.md)

## Context

ADR 0004 selected Node.js and strict TypeScript before backend service scaffolding began. CareerOS now standardizes backend services on Python so validation-heavy APIs, model boundaries and operational tooling share one Python ecosystem. No backend service scaffold or public runtime-specific contract has shipped yet, so the change can happen without a code or data migration.

The runtime decision must preserve independent services, strict validation, testability and the existing API/event contracts. It must not couple domain rules to HTTP, persistence, broker or provider frameworks.

## Decision

### Runtime

Backend services use Python 3.14. Each repository pins Python 3.14 and a current security patch consistently in development, CI and container builds. Python 3.15 is reconsidered after the required libraries and deployment images demonstrate stable support.

Dependencies and tool configuration live in `pyproject.toml` with a deterministic lockfile. V1-007 standardizes the package manager, formatter/linter, strict type checker and test commands before V1-009 creates the first service scaffold.

### Validation models

Pydantic v2 is the default for data-bearing models at API, event, configuration, command and adapter boundaries. Environment-backed configuration uses `pydantic-settings` and is validated once during startup.

Boundary models reject or deliberately version unknown fields, enforce domain-relevant constraints and expose stable serialized forms. Plain dictionaries and standard dataclasses do not replace validated boundary models. Secrets and sensitive fields are excluded or redacted before logging or serialization.

Pydantic is not required inside a deliberately framework-independent domain object that performs no parsing or serialization. This exception preserves the architecture dependency rule rather than creating an unvalidated external boundary.

### Architecture

Backend services use hexagonal architecture:

- domain rules and value semantics remain in the core;
- application use cases orchestrate authorization, transactions and domain behavior;
- the core defines narrow inbound and outbound ports around its needs;
- HTTP, persistence, messaging, identity and provider integrations are adapters;
- framework and vendor types are mapped at the edge and do not leak inward;
- use cases receive port implementations through explicit constructor injection;
- dependency wiring and concrete adapter construction stay in the composition root;
- schema migrations and their runner belong to the owning persistence adapter, and startup applies and verifies every migration head before accepting traffic.

SOLID principles and design patterns guide boundaries but do not justify speculative interfaces or abstractions. Composition is preferred to inheritance.

### Quality baseline

Every backend repository must provide deterministic commands for formatting/linting, strict type checking, unit tests and boundary integration tests. Reviews verify Pydantic validation failures, authorization denials, adapter failures, log redaction and the hexagonal dependency direction. CI remains the enforcement mechanism; the `code-quality-review` skill provides judgment-based PR review guidance.

## Consequences

- TypeScript remains appropriate for the web application and JavaScript-based workspace tooling, but not for V1 backend service implementations.
- V1-007 must encode the Python 3.14, Pydantic v2, hexagonal architecture and quality gates in the executable service checklist.
- V1-009 becomes the first reference Python service scaffold.
- Public OpenAPI, AsyncAPI and JSON Schema contracts remain language-neutral.
- Existing PostgreSQL, RabbitMQ, S3-compatible storage and Keycloak decisions are unchanged.

## Migration plan

1. Update the V1 plan and review skills before service scaffolding.
2. Deliver the executable Python service baseline in V1-007.
3. Apply the baseline to V1-009 and subsequent backend service repositories.
4. Reject Node.js backend scaffolds in review unless a later ADR explicitly changes this decision.

No service code, database migration or public contract migration is required because implementation has not started.

## Rejected alternatives

- Keeping Node.js for backend services is rejected by the revised product direction.
- Adopting Python 3.15 immediately is deferred because it is newly released and the V1 dependency set has not yet demonstrated compatibility.
- Using Pydantic models as ORM entities or forcing Pydantic into every pure domain object is rejected because it would couple the core to boundary and persistence concerns.
- Allowing each service to choose its own runtime is rejected because it would fragment scaffolding, CI and operational support.

## References

- [Status of Python versions](https://devguide.python.org/versions/)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)
- [Pydantic settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
