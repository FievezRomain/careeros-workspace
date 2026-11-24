# careeros-ai-gateway

Central model policy, redaction, quotas, audit metadata and fallbacks.

Repository: https://github.com/FievezRomain/careeros-ai-gateway

Example: expose a stable `extract-job-requirements` capability and route it to OpenAI, Claude or a local model according to policy, while normalizing schemas, errors, quotas and provenance. Provider-specific capabilities remain explicit.

## V1-020 capability boundary

- `POST /v1/capabilities/{capabilityId}/invocations` accepts a versioned,
  provider-neutral input envelope. It requires an authenticated caller with
  `ai:invoke` and a synthetic, opaque `Idempotency-Key`.
- The core-owned `CapabilityGateway` port receives only validated capability
  data. Provider clients remain outbound adapters and are constructor-injected
  by the composition root.
- Responses contain the capability and schema versions plus opaque model and
  prompt provenance. Consumers remain responsible for deterministic validation
  against verified facts and business rules.
- The V1-020 default composition rejects every token, exposes no provider route
  and refuses readiness until deployment authentication and a V1-021 provider
  adapter are injected.
- Request and response bodies, bearer tokens, tenant identifiers and account
  identifiers are excluded from structured request logs.

Provider schema validation and redaction belong to V1-021. Timeouts, quotas,
fallbacks, cost metadata and durable idempotent replay belong to V1-022.

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.
