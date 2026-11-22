# ADR 0003: Keycloak as the identity provider

- Status: accepted for V1
- Date: 2026-11-22

## Context

CareerOS needs sign-in, token issuance, account lifecycle and optional stronger authentication without embedding identity credentials in business services. An existing Vasco Admin setup demonstrates a safe local pattern with loopback-only exposure, isolated persistence, explicit provisioning and ignored local secrets.

## Decision

Use Keycloak as the V1 identity provider. Business services validate a normalized identity and authorization context; they do not depend on whether the realm is hosted in an existing trusted Keycloak installation or a dedicated CareerOS installation.

Adapt the Vasco Admin operating principles, not its identities or secrets:

- dedicated CareerOS realm and clients;
- placeholder configuration committed publicly, generated secrets ignored;
- local services bound to loopback;
- explicit, idempotent provisioning for an existing realm;
- synthetic local test identities only;
- no production administration endpoint exposed publicly by default.

## Consequences

The V1 infrastructure includes a local CareerOS realm and bootstrap documentation. Reusing an existing Keycloak instance later requires only environment and realm placement changes, while issuer and audience configuration remain explicit.
