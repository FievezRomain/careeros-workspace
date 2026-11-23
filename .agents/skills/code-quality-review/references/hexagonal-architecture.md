# Hexagonal architecture review profile

Apply this profile to backend services and substantial service-boundary changes. Small repository scripts, static configuration and UI components do not need artificial ports and adapters unless they cross a meaningful boundary.

## Dependency rule

Dependencies point inward:

```text
inbound adapters -> application/use cases -> domain
outbound adapters -> application ports <- application/use cases
```

The domain contains business invariants and value semantics. Application use cases coordinate domain behavior, authorization context and transaction boundaries. Ports describe what a use case needs or exposes. Adapters translate HTTP, events, persistence, clocks, identifiers, brokers and provider SDKs.

The core owns its ports. Do not define a port from the convenience methods of a framework or vendor SDK.

## Review criteria

- Domain modules do not import HTTP controllers, ORM models, broker clients, environment readers or provider SDKs.
- Application use cases receive dependencies through explicit ports and do not resolve them from global containers.
- Use cases never instantiate ORM engines, repositories, migration tools, HTTP clients or provider SDKs. The composition root creates concrete adapters and constructor-injects them through core-owned ports.
- Inbound adapters validate and map external data before invoking a use case.
- Outbound adapters map domain/application data to persistence or provider representations without leaking vendor types inward.
- Authorization and ownership checks occur in the use-case path, not only in controllers.
- Transaction scope belongs to the application use case and never spans databases owned by different services.
- Ports express narrow capabilities needed by use cases. Reject generic catch-all gateways and base repositories that erase domain intent.
- Domain events describe completed domain facts; integration events are versioned and mapped at the boundary.
- Framework bootstrapping and dependency wiring stay in the composition root.
- Migration scripts, configuration and runners live inside the owning persistence/migration adapter rather than at repository root or in the application layer. Changing the database adapter must not require moving or importing migration technology into the core.
- Persistent services invoke an injected migration-runner port during startup, apply all pending revisions and verify every expected head before accepting traffic. Readiness alone is not a substitute for migration completion.
- Cross-cutting logging, metrics and correlation do not expose sensitive payloads or make the domain depend on observability SDKs.

Do not require a fixed folder tree. Judge dependency direction and responsibility boundaries rather than directory names.

## Testing evidence

- Domain tests run without network, filesystem, database or framework startup.
- Use-case tests use small fakes or stubs for ports and cover success, validation and authorization-denial paths.
- Startup tests prove the injected migration runner is invoked, incomplete heads fail startup, and the real adapter can apply and roll back revisions against an isolated database.
- Adapter integration tests prove mapping, persistence, protocol and error translation.
- Public API/event contract tests verify compatibility independently of internal domain structure.
- Architecture tests or dependency rules should prevent inward layers from importing adapters when the repository tooling supports them.

## Common findings

- ORM or transport models used as domain entities.
- Controllers containing domain policy or transaction orchestration.
- Use cases importing concrete database/provider clients.
- Use cases constructing adapters directly or resolving them from service locators instead of constructor injection.
- Root-level migration trees with unclear adapter ownership, or migration commands that are never enforced during application startup.
- One generic service class accumulating unrelated use cases.
- Ports mirroring vendor SDKs instead of domain needs.
- Pydantic, framework decorators or validation schemas leaking into a deliberately framework-independent Python domain.
- Interfaces added for every class despite no boundary or alternate implementation.
