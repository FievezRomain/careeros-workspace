# Shared contracts

Place versioned OpenAPI, AsyncAPI and JSON Schema contracts here when implementations are introduced.

All contracts follow the [CareerOS contract conventions](conventions.md).

Validate locally from the workspace root with `npm ci && npm run contracts:check`. On a pull request, `npm run contracts:compat -- <base-sha>` also rejects removals, narrowed enums, newly required fields and stable type/reference changes within the same major contract. References must resolve to repository-local files so CI remains deterministic. Intentional breaking changes require a new major-version path and a documented migration.

Rules:

- Prefer additive changes.
- Document deprecation and migration windows.
- Validate producers and consumers in CI.
- Never include real user payloads; examples are fictitious and minimal.
