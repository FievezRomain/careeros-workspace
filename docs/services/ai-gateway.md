# careeros-ai-gateway

Central model policy, redaction, quotas, audit metadata and fallbacks.

Repository: https://github.com/FievezRomain/careeros-ai-gateway

Example: expose a stable `extract-job-requirements` capability and route it to OpenAI, Claude or a local model according to policy, while normalizing schemas, errors, quotas and provenance. Provider-specific capabilities remain explicit.

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.
