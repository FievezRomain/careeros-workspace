# careeros-matching-service

Explainable ranking of profile/job snapshot pairs.

Repository: https://github.com/FievezRomain/careeros-matching-service

## V1-023 deterministic scoring

`POST /v1/internal/matches/score` evaluates one confirmed profile snapshot and
one opportunity version for an account-bound caller with `matching:score`.
The stateless result includes the scorer version, evidence for each known
finding, unassessed requirements, hard conflicts and the score limitation.
Mandatory requirements have greater weight. A link-only opportunity remains
unscored until source requirements can be verified. See the service overview
and `/openapi.json` for the payload contract.

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.
