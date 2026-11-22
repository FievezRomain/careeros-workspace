# ADR 0001 â€” Multi-repository workspace with Git submodules

## Status

Accepted.

## Decision

Each deployable CareerOS component has an independent repository, history, release cadence and CI. `careeros-workspace` references them as Git submodules and owns cross-cutting documentation, contracts and Codex skills.

## Consequences

- A single recursive clone provides complete system context.
- Service releases remain independent.
- Submodule updates are explicit and reviewable.
- Cross-repository changes require coordinated contract and documentation updates.