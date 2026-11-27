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

## V1-024 requirement extraction

`POST /v1/internal/requirements/extract` uses the AI gateway's versioned
`extract-job-requirements` capability for a single owned opportunity version.
The service checks each source excerpt, records extraction provenance and keeps
suggestions separate from confirmed scoring inputs. Link-only opportunities are
unassessed. See the service OpenAPI and BR-MAT-003 and BR-AI-002.

## V1-025 score explanation

The scoring response shows each requirement's contribution and the confirmed level
behind it. The versioned explanation exposes evidence coverage and hypothetical
score bounds over the same requirements. Link-only opportunities carry an explicit
reason for lacking a score or bounds. See BR-MAT-003 through BR-MAT-006.

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.
