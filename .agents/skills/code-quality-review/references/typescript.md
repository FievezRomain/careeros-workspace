# TypeScript quality profile

CareerOS uses TypeScript for the web application and JavaScript-based workspace tooling. Backend services use Python under ADR 0005.

## Types and validation

- Keep strict mode enabled. Do not introduce `any`, non-null assertions or unchecked casts to silence a design problem.
- Receive untrusted data as `unknown` and validate it at HTTP, event, configuration, database-adapter and provider boundaries.
- Prefer schemas derived from the versioned contract or the repository's established validation library. Do not create a second competing schema source.
- Use discriminated unions for state-dependent data and exhaustive checks for state transitions.
- Prefer `readonly` data for facts, snapshots, events and audit records.
- Distinguish missing, optional and nullable values deliberately.

## Structure

- Apply the hexagonal dependency rule: domain and application use cases do not import web frameworks, persistence clients, broker clients or provider SDKs.
- Define ports around domain capabilities and use-case needs; adapters implement those ports and map transport/persistence models at the edge.
- Inject clocks, identifiers, repositories and external clients when deterministic behavior or testing requires it.
- Use typed error objects and translate them once at the transport boundary.
- Avoid mutable process globals, import-time side effects and direct environment reads outside the configuration module.
- Preserve async errors and cancellation/timeouts; do not leave floating promises.

## Patterns

- Use Adapter for infrastructure/provider boundaries and Strategy for real policy alternatives.
- Use Repository where it protects service-owned persistence semantics, not as a generic CRUD wrapper.
- Prefer functions and composition to inheritance. Reject service locators, hidden singletons and speculative abstract factories.

## Verification

Run the repository's formatter, linter, type checker, unit tests and boundary/contract tests.

Check that tests cover:

- runtime validation of malformed external input;
- domain success and failure paths;
- authorization denial where applicable;
- migration and contract compatibility;
- timeouts and adapter failures without live providers;
- log redaction and stable error envelopes.
