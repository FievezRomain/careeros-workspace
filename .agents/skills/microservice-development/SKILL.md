---
name: microservice-development
description: Implement or modify a CareerOS service while preserving its responsibility boundary, authorization checks, contracts, observability and tests.
---

# Microservice development

Read the target repository's `AGENTS.md` and `docs/overview.md` first.

- Keep business rules independent from transport and provider adapters.
- Enforce authentication, ownership and tenant isolation at entry points.
- Make retryable commands idempotent and expose health and readiness signals.
- Use structured logs with correlation IDs and redaction.
- Update tests, service documentation and affected contracts in the same change.