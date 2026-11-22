# CareerOS Workspace

Central workspace for the CareerOS open-source system. It brings together architecture, service documentation, shared contracts, Codex skills and all product repositories as Git submodules.

## Clone

```bash
git clone --recurse-submodules https://github.com/FievezRomain/careeros-workspace.git
```

For an existing clone:

```bash
git submodule update --init --recursive
```

## Repository map

| Area | Repository |
| --- | --- |
| Workspace | `careeros-workspace` |
| Web application | `careeros-web` |
| Identity | `careeros-identity-service` |
| Professional profile | `careeros-profile-service` |
| Job catalog | `careeros-job-service` |
| Matching | `careeros-matching-service` |
| Resume generation | `careeros-resume-service` |
| ATS validation | `careeros-ats-service` |
| Applications | `careeros-application-service` |
| Communication | `careeros-communication-service` |
| Analytics | `careeros-analytics-service` |
| AI gateway | `careeros-ai-gateway` |
| Automation | `careeros-automation` |
| Infrastructure | `careeros-infrastructure` |

## Safety

No secret, real CV, real application, provider credential or personal data belongs in any public CareerOS repository. See `SECURITY.md` and the `security-privacy` skill.

## Status

Initial architecture and contribution baseline. Services are intentionally separated so each can evolve and release independently.

## License

Apache-2.0.