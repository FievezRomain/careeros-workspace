# CareerOS Workspace

Central workspace for the CareerOS open-source system. It brings together architecture, functional rules, service documentation, shared contracts, Codex skills and all product repositories as Git submodules.

## Clone

```bash
git clone --recurse-submodules https://github.com/FievezRomain/careeros-workspace.git
```

For an existing clone:

```bash
git submodule update --init --recursive
```

## Product source of truth

- [V1 development plan](docs/product/v1-development-plan.md)
- [Functional business-rule catalog](docs/business-rules/catalog.md)
- [System overview](docs/architecture/system-overview.md)
- [Architecture decisions](docs/decisions/)

Business rules describe observable product behavior without implementation details. The `careeros-acceptance-tests` repository provides their executable cross-service traceability and V1 non-regression gate.

## Repository map

| Area | Repository |
| --- | --- |
| Workspace and functional rules | `careeros-workspace` |
| Acceptance and non-regression | `careeros-acceptance-tests` |
| Web application | `careeros-web` |
| Identity | `careeros-identity-service` |
| Professional profile | `careeros-profile-service` |
| Job catalog | `careeros-job-service` |
| Matching | `careeros-matching-service` |
| Resume generation | `careeros-resume-service` |
| ATS validation | `careeros-ats-service` |
| Applications | `careeros-application-service` |
| Communication and notifications | `careeros-communication-service` |
| Analytics | `careeros-analytics-service` |
| AI gateway | `careeros-ai-gateway` |
| Automation | `careeros-automation` |
| Infrastructure | `careeros-infrastructure` |

## Safety

No secret, real CV, real application, provider credential or personal data belongs in any public CareerOS repository. See `SECURITY.md` and the `security-privacy` skill.

## Status

V1 planning and executable architecture baseline. Services are intentionally separated so each can evolve and release independently.

## License

Apache-2.0.
