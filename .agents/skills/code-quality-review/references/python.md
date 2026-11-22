# Python quality profile

CareerOS backend services use Python 3.14 and Pydantic v2. The target repository's `pyproject.toml` and lockfile are authoritative for the pinned patch and tooling.

## Models and validation

- Prefer Pydantic `BaseModel` for data-bearing models that cross API, event, configuration, provider, command or persistence-adapter boundaries.
- Use `pydantic-settings` `BaseSettings` for environment-backed configuration. Require values explicitly, validate at startup and never print secret values.
- Boundary DTOs must not use plain dictionaries or standard dataclasses in place of runtime validation.
- Default external-input models to rejecting unknown fields when compatibility permits. Make extension behavior deliberate and versioned.
- Use constrained fields and field validators for local invariants; use model validators only for genuine cross-field rules.
- Prefer immutable models for snapshots, facts, audit records and other values whose identity depends on their content.
- Treat `model_dump()` output as potentially sensitive. Redact before logging and avoid serializing secrets by default.
- Test both accepted input and representative `ValidationError` paths.

Pydantic is the default for Python data models, not a replacement for every object. In a hexagonal service, use it systematically for inbound/outbound DTOs, application-port data, configuration and validated adapter input. A plain class or frozen dataclass is acceptable inside the pure domain when avoiding a Pydantic dependency preserves the inward dependency rule and the object has no parsing or serialization responsibility. Such exceptions should be intentional and easy to explain in review. ORM entities follow the chosen persistence library and map through validated boundary models.

## Types and structure

- Type all public functions and important internal boundaries. Avoid `Any`; contain unavoidable dynamic values behind `object`, protocols and explicit narrowing.
- Prefer `Protocol` for dependency contracts and constructor injection for adapters.
- Keep domain logic independent from HTTP, Pydantic transport models, database and provider SDK details.
- Use explicit exceptions with stable translation at the transport boundary. Do not use exceptions for ordinary branching.
- Use context managers for resource lifetimes and cancellation-aware timeouts for external I/O.
- Avoid mutable module globals, import-time network calls and hidden environment reads.

## Patterns

- Use Adapter for providers and infrastructure clients, Strategy for genuine interchangeable policy, and Repository only when it protects a persistence boundary.
- Add Unit of Work only when one use case coordinates an atomic transaction in one owned database.
- Reject service locators, global clients, deep inheritance and generic base repositories that erase domain semantics.

## Verification

Run the repository-configured formatter/linter, type checker and tests. Typical tools are Ruff, mypy or Pyright, and pytest, but do not add them during a review unless the story includes tooling.

Check that tests cover:

- valid and invalid Pydantic inputs;
- missing or malformed configuration;
- domain invariants and error translation;
- authorization denial where applicable;
- adapter timeouts and failures without live providers;
- logs and errors that do not expose sensitive values.
