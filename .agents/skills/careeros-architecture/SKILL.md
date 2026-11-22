---
name: careeros-architecture
description: Review or change CareerOS system boundaries, dependencies, cross-service flows and architecture decisions. Use for work spanning multiple repositories or deciding which service owns a capability.
---

# CareerOS architecture

Read `../../../docs/architecture/system-overview.md`, the relevant service documents and existing ADRs.

- Assign each capability and data set to one owning service.
- Keep services independently deployable and avoid shared databases.
- Prefer versioned APIs for queries and versioned events for asynchronous state changes.
- Record consequential cross-service decisions as ADRs.
- Identify affected contracts, consumers, security boundaries and migration steps before implementation.