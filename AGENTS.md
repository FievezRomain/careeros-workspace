# CareerOS agent entrypoint

Start with `README.md`, `docs/architecture/system-overview.md`, the target service document under `docs/services/`, and the target repository's own `AGENTS.md`.

## Routing

- Architecture or service boundaries: use `careeros-architecture`.
- Service implementation: use `microservice-development` plus the target service documentation.
- OpenAPI, schemas or compatibility: use `api-contracts`.
- Events, queues, retries or idempotency: use `event-driven-design`.
- Model calls, prompts or evaluation: use `ai-engineering`.
- Resume generation or ATS reports: use `ats-resume-validation`.
- Credentials, privacy, tenancy or logging: use `security-privacy`.
- Tests and release quality: use `testing-quality`.
- Documentation maintenance: use `documentation`.
- n8n workflows: use `n8n-workflows`.

## System invariants

- Never commit secrets, real CVs, real applications or personal data.
- Services do not share databases. Integration happens through versioned APIs and events.
- Authorization and ownership checks happen at every service boundary.
- AI output is untrusted until validated against verified profile facts and deterministic rules.
- ATS scores are internal diagnostics, not guarantees about third-party screening systems.
- External messages, calendar changes and application submissions require explicit user approval at action time.
- Update service documentation and contracts together with behavioral changes.
- Every new, changed or deprecated business behavior must update `docs/business-rules/catalog.md` with its stable `BR-...` identifier in the same delivery.
- Every new or changed business rule must add or update an executable scenario in `careeros-acceptance-tests`; documentation-only coverage does not count.
- Update the acceptance repository first, then update the workspace `acceptance-tests` submodule pointer to the tested commit. Never add a new rule to the frozen uncovered-rule baseline.
- Run `npm run coverage:no-new-gaps` in `acceptance-tests` against the canonical workspace catalog before marking a story complete.
