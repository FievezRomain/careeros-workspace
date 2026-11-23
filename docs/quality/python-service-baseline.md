# Python service quality baseline

CareerOS backend services use Python 3.14, Pydantic v2 and inward-facing hexagonal dependencies. TypeScript remains limited to the web application and workspace tooling.

## Deterministic gate

Each service declares `[tool.careeros.quality]` in `pyproject.toml`. Run:

```text
python scripts/check_service_quality.py <service-root>
```

The declaration identifies the package, domain, application, ports, adapters and composition root; whether persistence is used; executable format, lint, strict type, test, secret and security commands; migration up/down commands and apply/rollback evidence when applicable; and unit, integration, contract, health, logging and authorization evidence. Persistent services additionally declare an adapter-owned migration directory, its runner and startup-migration evidence. Logging declares structured output, correlation and redaction as mandatory controls.

The checker also requires a lockfile, Pydantic boundary models, `pydantic-settings`, and rejects infrastructure/framework imports from domain or application code. Boundary DTOs, settings and messages use Pydantic models. Plain classes remain valid for behavior-rich domain objects; `dataclasses` are not accepted as adapter-boundary data models.

Each service CI must execute both this workspace checker and every declared command. A successful declaration is not a substitute for running its commands. Domain and application modules may depend on core-owned ports but not ORM, migration or provider libraries. Use cases receive adapters through constructor injection, and only the composition root creates concrete implementations.

Migrations belong under the owning adapter rather than at repository root. Persistent services inject a migration runner into application startup, apply every pending revision, verify all expected heads and fail before serving traffic when migration cannot complete. Tests must prove startup invocation and incomplete-head refusal plus upgrade and rollback against an isolated database. Logging tests must prove correlation propagation and sensitive-payload redaction.

## Review gate

Deterministic failures belong in CI. Reviewers use the `code-quality-review` skill for correctness, SOLID trade-offs, justified patterns, maintainability and hexagonal boundaries, and add the domain or security skill when relevant. Findings use P0 (release/security blocker), P1 (major correctness), P2 (maintainability or design risk) and P3 (minor improvement).

Automatic Codex review is repository configuration, not a workflow secret:

1. connect the GitHub repository in Codex settings;
2. enable **Automatic review** under **Review code** for the repository and personal preferences;
3. keep repository-specific judgment rules under `## Code Review Rules` in the nearest `AGENTS.md`;
4. validate setup on a representative PR with `@codex review`.

Branch protection keeps deterministic CI and required human approvals authoritative. P0/P1 findings must be resolved before completion. Codex review is an additional reviewer, never a replacement for tests or ownership approval.
