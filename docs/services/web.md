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
Feature content remains placeholder-only until its owning V1 story is delivered; this increment
does not add profile, job or application business behavior.
