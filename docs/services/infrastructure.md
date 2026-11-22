# careeros-infrastructure

Local development and deployment configuration without secrets.

Repository: https://github.com/FievezRomain/careeros-infrastructure

Initial scope: Docker Compose, health checks, local networks, reverse proxy and observability. Idempotent install, migration, backup and restore scripts can be added when needed; heavier orchestration is introduced only when justified.

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.
