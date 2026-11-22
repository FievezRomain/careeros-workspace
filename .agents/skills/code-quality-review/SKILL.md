---
name: code-quality-review
description: Review CareerOS pull requests and implementation changes for correctness, maintainability, language conventions, SOLID design, appropriate patterns and test evidence. Use for code-quality audits and PR reviews; combine it with the relevant domain or security skill when those boundaries are in scope.
---

# CareerOS code quality review

Review the changed behavior, not just formatting. Prefer a small correct design over pattern-heavy code.

## Review workflow

1. Read the target repository's `AGENTS.md`, architecture/service document and language configuration.
2. Inspect the diff plus affected callers, contracts, migrations and tests. Do not infer quality from the diff alone when behavior crosses a boundary.
3. Load the matching language profile:
   - For Python, read [references/python.md](references/python.md).
   - For TypeScript or JavaScript web/tooling changes, read [references/typescript.md](references/typescript.md).
   - For backend service structure or boundary changes, also read [references/hexagonal-architecture.md](references/hexagonal-architecture.md).
4. Run the repository's existing formatter, linter, type checker and focused tests when available. Do not introduce a new tool merely to complete a review.
5. Report actionable findings with evidence. Separate blocking defects from non-blocking improvements and name any checks that could not run.

## Review priority

Evaluate in this order:

1. correctness, security, authorization, tenant isolation and data safety;
2. API/event compatibility, persistence ownership and migration safety;
3. validation, error handling, observability and deterministic behavior;
4. meaningful test coverage, including failure and denial paths;
5. cohesion, coupling, readability and unnecessary complexity;
6. language conventions and repository tooling.

Do not block a PR for a personal style preference already handled by formatters or for a hypothetical abstraction with no demonstrated variation.

## Design criteria

- Apply SOLID as diagnostic questions, not as a demand for one interface or class per concept.
- Structure backend services with hexagonal boundaries: domain and use cases remain inside; transport, persistence, messaging and provider SDKs remain adapters outside.
- Keep responsibilities cohesive and dependencies directed toward stable domain boundaries.
- Prefer composition and explicit dependency injection over inheritance, service locators, mutable globals or hidden singletons.
- Introduce Adapter, Strategy, Repository, Unit of Work or similar patterns only when they isolate a real boundary or change axis. Flag pattern theatre and speculative generalization.
- Keep functions and modules small enough to understand, but do not split code solely to satisfy a line-count rule.
- Make invalid states difficult to construct. Validate untrusted input once at the boundary and keep internal types precise.
- Use typed, stable errors at public boundaries. Do not leak stack traces, credentials, personal data or raw provider payloads.
- Avoid broad refactors, unrelated dependency upgrades and formatting sweeps in a focused story.

## CareerOS gates

- Backend services use Python 3.14, Pydantic v2 and hexagonal architecture. TypeScript is reserved for the web application and JavaScript-based workspace tooling unless a later ADR says otherwise.
- Every service boundary enforces authentication, ownership and tenant isolation.
- Services do not share databases; integration uses versioned APIs or events.
- AI and external input remain untrusted until deterministic validation succeeds.
- New or changed business behavior updates the stable `BR-...` catalog entry and executable acceptance scenario in the same delivery.
- Tests and examples use synthetic data only. Repositories contain no secrets, real resumes, applications or personal data.

## PR review output

For each finding, provide:

- severity (`P0` to `P3`);
- a short defect-oriented title;
- exact file and tight line range;
- the concrete failure mode or maintenance cost;
- the smallest safe correction.

Only report issues caused or exposed by the change. If there are no actionable findings, say so and list residual risks or unexecuted checks briefly. A review is read-only unless the user explicitly requests fixes.
