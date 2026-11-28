# careeros-web

User interface; no secrets or autonomous external actions.

Repository: https://github.com/FievezRomain/careeros-web

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.

## V1 application shell

- The browser application is a React/TypeScript SPA built with Vite and consumes only versioned
  service APIs.
- Authentication uses OIDC Authorization Code with PKCE. The SPA is a public client and never
  contains a client secret.
- The OIDC adapter keeps user and transaction state in `sessionStorage`; raw tokens are not
  exposed to presentation components, URLs, rendered markup, logs or analytics.
- Every `/app` route is guarded by restored session state. Loading and restoration failures render
  no private shell, and anonymous sessions return to the public sign-in entry.
- Post-authentication navigation accepts only local `/app` paths, preventing external open
  redirects.
- The session adapter implements a local port injected through the authentication provider, so UI
  tests use deterministic fakes and never contact a live identity provider.

## Current navigation

The authenticated shell exposes Overview, Profile, Jobs, Resumes and Applications navigation.
Profile and Jobs expose their owned records. Resumes and Applications remain
protected placeholders until their owning V1 stories are delivered.

## V1 profile onboarding

- `/app/profile` loads and edits owned experiences, education items and self-declared skills through
  the versioned profile API.
- Presentation code depends on a local `ProfilePort`. The HTTP adapter receives the access-token
  capability through dependency injection and validates successful API responses before rendering;
  raw tokens never enter components.
- The editor validates required values, chronological dates and current-item state before transport.
  The profile service remains authoritative for scopes, ownership and domain validation.
- Loading, empty, success, validation, service-error and authorization-denial states are explicit.
  Authorization denial renders no profile facts or provider payload details.

## V1 automatic-search controls

- The protected profile view lets an authenticated person activate, update, pause and resume their
  automatic opportunity search through the versioned profile API.
- The UI displays active or paused state, immutable criteria version, timezone and daily window.
  Before activation it shows the explicit `Europe/Paris`, `08:00`–`10:00` default.
- Every mutation sends a fresh idempotency key, and successful responses are validated at the HTTP
  adapter boundary before they reach presentation components.
- The view explains that role, skill, experience, location, work-preference and criteria changes
  request rematching, while contact-only and presentation-only changes do not. The profile service
  remains authoritative for ownership, validation and that classification.

## V1 job catalog and recommendations

- `/app/jobs` presents the matching service's ordered recommendations.
  `/app/jobs/catalog` shows the owned catalog and `/app/jobs/:id` opens an
  immutable opportunity version with source provenance and verification state.
- The web adapter reads `GET /v1/jobs`, `GET /v1/jobs/{opportunityId}`,
  `GET /v1/recommendations` and `GET /v1/recommendations/{groupId}`.
  The OIDC client requests `jobs:read` and `matching:recommendations:read`.
- The detail shows matching evidence only when the job group and evaluated version
  agree with the owned job response. Matching supplies the findings, weights,
  uncertainty, eligibility reason and score limitation.
- The gateway routes `/api/jobs` and `/api/matching` to the corresponding service
  and strips the prefix. Absolute gateway URLs can be configured through
  `VITE_JOB_API_BASE_URL` and `VITE_MATCHING_API_BASE_URL`.
