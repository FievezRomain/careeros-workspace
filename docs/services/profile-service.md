# careeros-profile-service

Canonical verified professional profile and preferences.

Repository: https://github.com/FievezRomain/careeros-profile-service

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.

## V1 profile-fact boundary

- Experience, education and skill facts expose server-recorded provenance and a closed
  `unconfirmed` or `userConfirmed` validation status.
- Direct entries start confirmed. Resume imports and generated suggestions remain unconfirmed
  until the owner explicitly confirms the current value.
- Replacements are recorded as user corrections by the service; clients cannot claim this
  provenance themselves.
- Immutable snapshots capture fact values, provenance and confirmation status atomically. Later
  profile changes never rewrite a snapshot already selected by another artifact.
- Snapshot creation follows the shared idempotency convention with a minimum 24-hour outcome
  retention. Reads and mutations always filter by both trusted tenant and account identifiers.

## Delivery order and consumers

The additive OpenAPI 1.1 contract is published before the profile-service producer rollout.
Resume and matching consumers may adopt snapshot identifiers only after the producer is deployed;
they must continue to accept the existing live-profile contract during that rollout. No consumer
may read the profile database or reconstruct provenance outside this service.
