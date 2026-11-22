# CareerOS V1 Development Plan

## V1 outcome

A user can authenticate, build a verified professional profile, record a job opportunity, obtain an explainable match, generate a grounded resume, validate the final document with ATS rules, approve an application package, track its state, prepare an approved follow-up and view a privacy-conscious conversion funnel.

V1 does not attempt generic browser automation against arbitrary job boards. External messages or submissions are executed only through an explicitly supported adapter and after action-time user approval.

## V1 scope

V1 includes one reviewable end-to-end journey that lets a user:

- authenticate and access only resources they own;
- maintain a professional profile whose facts carry validation status and provenance;
- capture and normalize a job opportunity with its source provenance;
- receive an explainable match based on versioned profile and job snapshots;
- generate one ATS-safe PDF template and a DOCX export using verified facts only;
- obtain a versioned ATS report with deterministic findings, evidence and honest limitations;
- create, approve and track an application package without autonomous submission;
- prepare and explicitly approve a follow-up before delivery through one supported adapter;
- receive in-app notifications and, after explicit account linking, Telegram Bot notifications;
- view privacy-conscious funnel aggregates that exclude raw resume and application content.

## V1 non-goals

V1 explicitly excludes:

- generic browser automation or support for arbitrary job boards;
- autonomous, bulk or approval-free applications, messages and calendar changes;
- facts invented by a model, unvalidated model output or claims that an ATS score predicts a third-party screening decision;
- email delivery and WhatsApp integration;
- multiple resume templates, broad provider coverage or a marketplace of delivery adapters;
- cross-service database access, shared service schemas or unversioned public integration contracts;
- multi-region operation, internet-scale capacity and production availability guarantees.

## V1 quality attributes

- **User control:** every consequential external action requires explicit approval at action time.
- **Security and isolation:** authentication context, authorization and ownership are validated at every service boundary; each service owns isolated persistence.
- **Privacy:** logs redact sensitive payloads, analytics minimize stored data, and repositories and tests contain only synthetic fixtures.
- **Grounding and explainability:** generated content is traceable to verified profile facts, rankings expose evidence and uncertainty, and ATS findings state their limits.
- **Reliability:** external side effects are idempotent, retry-safe and auditable; deterministic rules remain the authority for validation and state transitions.
- **Interoperability:** public APIs, events and schemas are versioned, and services integrate only through those contracts.
- **Testability:** the complete journey is reproducible through black-box acceptance tests without direct database access or live provider side effects.
- **Operability:** services expose health and readiness signals, propagate correlation identifiers without sensitive content, and the release includes a tested backup and restore procedure.

## V1 success criteria

V1 is ready to release only when all of the following are true:

1. A synthetic user completes the full V1 journey through public contracts in the repeatable black-box acceptance suite.
2. Acceptance coverage includes the journey's success path plus applicable validation failures and authorization denials, and `coverage:no-new-gaps` reports no newly uncovered business rule.
3. No application, message or other consequential external action can occur without a current explicit approval; repeated delivery requests do not duplicate the side effect.
4. Generated resume content is validated against verified profile facts, and match and ATS results retain evidence, provenance and limitations.
5. Service, contract, security and documentation checks pass in CI with no committed secret or real personal, resume or application data.
6. The V1 security review finds no unresolved release-blocking authorization, tenancy, privacy, secret-handling or audit issue.
7. The documented backup and restore smoke test succeeds for the V1 system-of-record data and artifact metadata.
8. Known limitations are published, all V1 pull requests respect the delivery budget or document an approved split, and the release checklist is complete.

## V1 architecture decisions

- PostgreSQL is the default system of record for V1 business data. Each service owns its database or isolated database namespace and credentials; no service reads another service's tables. JSONB is reserved for source payloads and other genuinely semi-structured values.
- Resume files and generated documents live in S3-compatible object storage, not in relational columns. Messaging and cache technologies are introduced only for their documented responsibilities.
- Keycloak is the identity provider. CareerOS can target a dedicated realm in an existing trusted Keycloak installation or a separate installation without changing service authorization contracts.
- The functional source of truth is `docs/business-rules/catalog.md`. Executable cross-service scenarios live in `careeros-acceptance-tests` and reference stable business-rule identifiers.
- Notifications are channel-neutral. The free V1 baseline is an in-app history plus Telegram Bot notifications after explicit account linking. `careeros-communication-service` owns preferences and notification intent; a credential-free workflow definition in `careeros-automation` delivers through n8n's Telegram node. Email is excluded. WhatsApp is outside V1 unless a genuinely no-cost, policy-compliant path is verified later.

## Delivery model

- Work directly in the existing repositories cloned as submodules under `C:\DEV\careeros-workspace`; do not create Codex worktrees.
- Deliver one user story on one dedicated branch in its owning repository whenever possible.
- Branch format: `story/v1-NNN-short-slug`.
- Commit format: Conventional Commits, scoped when useful.
- Every completed story is pushed and opened as a pull request linked to the central workspace issue.
- Cross-repository work starts with the contract or ADR PR in `careeros-workspace`; service PRs follow independently. The workspace submodule pointer is updated in a final, small coordination PR.
- Target pull request budget: at most 400 changed lines excluding lockfiles/generated artifacts, at most 8 hand-edited files, and at most one database migration. Split the story when the budget is exceeded.
- No feature branch may contain unrelated refactors, dependency upgrades or formatting sweeps.

## Workflow states

`Backlog → Ready → In progress → In review → Validated → Done`

A story is **Ready** when its owner repository, dependencies, acceptance criteria and contracts are known. It is **Done** when tests and documentation pass, security constraints are checked, the PR is merged, and any affected workspace submodule pointer is updated.

## Epic 0 — Foundations and executable architecture

### Feature 0.1 — V1 decisions and contracts

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-001 | `careeros-workspace` | `story/v1-001-v1-scope` | Freeze V1 scope, non-goals, quality attributes and success criteria. |
| V1-002 | `careeros-workspace` | `story/v1-002-runtime-adr` | ADR for backend runtime, persistence isolation, broker, object storage and identity provider. |
| V1-003 | `careeros-workspace` | `story/v1-003-contract-conventions` | Define API/event versioning, error envelope, idempotency and correlation conventions. |

### Feature 0.2 — Local platform

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-004 | `careeros-infrastructure` | `story/v1-004-compose-dependencies` | Compose stack for databases, broker and object storage with placeholder configuration. |
| V1-005 | `careeros-infrastructure` | `story/v1-005-routing-health` | Local routing, service networks and health/readiness checks. |
| V1-006 | `careeros-infrastructure` | `story/v1-006-bootstrap-env` | Idempotent bootstrap and environment validation scripts. |
| V1-048 | `careeros-infrastructure` | `story/v1-048-keycloak-local` | Reusable local Keycloak realm, loopback-only Compose stack and safe bootstrap principle adapted from Vasco Admin. |

### Feature 0.3 — Service quality baseline

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-007 | `careeros-workspace` | `story/v1-007-service-checklist` | Executable service checklist covering layout, tests, migrations, logs and security gates. |
| V1-008 | `careeros-workspace` | `story/v1-008-contract-ci` | CI validation for OpenAPI, AsyncAPI and JSON Schema contracts. |

### Feature 0.4 — Business rules and executable conformance

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-049 | `careeros-workspace` | `story/v1-049-business-rules-catalog` | Dedicated functional business-rule catalog with stable identifiers, examples and traceability policy. |
| V1-050 | `careeros-acceptance-tests` | `story/v1-050-conformance-harness` | Black-box acceptance harness and rule-to-scenario traceability validation. |
| V1-054 | `careeros-workspace` | `story/v1-054-business-rule-traceability` | Mandatory workspace invariant and CI gate requiring catalog updates plus executable acceptance coverage for every new business rule. |

## Epic 1 — Identity, profile and onboarding

### Feature 1.1 — Identity and access

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-009 | `careeros-identity-service` | `story/v1-009-identity-scaffold` | Service scaffold, configuration validation and health endpoints. |
| V1-010 | `careeros-identity-service` | `story/v1-010-auth-context` | Validate identity tokens and expose a normalized account context. |
| V1-011 | `careeros-identity-service` | `story/v1-011-authorization-policy` | Ownership/tenant authorization policy with denial-path tests. |

### Feature 1.2 — Verified professional profile

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-012 | `careeros-profile-service` | `story/v1-012-profile-scaffold` | Service scaffold, isolated persistence and migrations. |
| V1-013 | `careeros-profile-service` | `story/v1-013-profile-crud` | Profile CRUD for experience, education and skills. |
| V1-014 | `careeros-profile-service` | `story/v1-014-profile-provenance` | Fact provenance, validation status and immutable profile snapshots. |

### Feature 1.3 — Web onboarding

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-015 | `careeros-web` | `story/v1-015-web-shell-auth` | Application shell, authenticated session and protected navigation. |
| V1-016 | `careeros-web` | `story/v1-016-profile-onboarding` | Profile onboarding/editor with loading, validation and error states. |

## Epic 2 — Jobs, AI gateway and matching

### Feature 2.1 — Job catalog

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-017 | `careeros-job-service` | `story/v1-017-job-scaffold` | Service scaffold, isolated persistence and migrations. |
| V1-018 | `careeros-job-service` | `story/v1-018-manual-job-import` | Manual job capture with raw source and provenance. |
| V1-019 | `careeros-job-service` | `story/v1-019-job-normalization` | Deterministic normalization, deduplication and query API. |

### Feature 2.2 — Provider-neutral AI access

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-020 | `careeros-ai-gateway` | `story/v1-020-ai-capability-contract` | Gateway scaffold and provider-neutral capability contract. |
| V1-021 | `careeros-ai-gateway` | `story/v1-021-provider-adapter` | First provider adapter with schema validation and redaction. |
| V1-022 | `careeros-ai-gateway` | `story/v1-022-ai-policy-observability` | Timeouts, fallback policy, quotas and non-sensitive observability. |

### Feature 2.3 — Explainable matching

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-023 | `careeros-matching-service` | `story/v1-023-matching-scaffold` | Service scaffold and deterministic baseline scoring. |
| V1-024 | `careeros-matching-service` | `story/v1-024-requirement-extraction` | Versioned requirement extraction through the AI gateway. |
| V1-025 | `careeros-matching-service` | `story/v1-025-match-explanation` | Evidence-based score explanation and uncertainty. |
| V1-026 | `careeros-web` | `story/v1-026-job-match-ui` | Job catalog, job detail and match explanation UI. |

## Epic 3 — Resume generation and ATS validation

### Feature 3.1 — Grounded resume generation

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-027 | `careeros-resume-service` | `story/v1-027-resume-scaffold` | Service scaffold, document versioning and artifact metadata. |
| V1-028 | `careeros-resume-service` | `story/v1-028-grounded-resume` | Generate content exclusively from verified profile facts. |
| V1-029 | `careeros-resume-service` | `story/v1-029-document-rendering` | Render and store one ATS-safe PDF template and DOCX export. |

### Feature 3.2 — ATS report

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-030 | `careeros-ats-service` | `story/v1-030-ats-extraction` | Service scaffold and final PDF/DOCX text extraction. |
| V1-031 | `careeros-ats-service` | `story/v1-031-ats-structure-rules` | Deterministic structural/readability checks and technical score. |
| V1-032 | `careeros-ats-service` | `story/v1-032-ats-relevance-report` | Versioned relevance findings with evidence and honest limitations. |
| V1-033 | `careeros-web` | `story/v1-033-resume-ats-ui` | Resume preview, ATS findings and regeneration action. |

## Epic 4 — Applications, communication and follow-up

### Feature 4.1 — Application CRM

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-034 | `careeros-application-service` | `story/v1-034-application-scaffold` | Service scaffold and application state machine. |
| V1-035 | `careeros-application-service` | `story/v1-035-approval-audit` | Explicit approval record and immutable audit references. |
| V1-036 | `careeros-application-service` | `story/v1-036-status-tracking` | Manual application status transitions and history API. |

### Feature 4.2 — Approved communication

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-037 | `careeros-communication-service` | `story/v1-037-message-draft` | Message draft model and preview API without delivery. |
| V1-038 | `careeros-communication-service` | `story/v1-038-approved-delivery` | One delivery adapter gated by approval and idempotency. |
| V1-039 | `careeros-automation` | `story/v1-039-followup-workflow` | Credential-free n8n follow-up workflow with approval gate and retries. |
| V1-040 | `careeros-web` | `story/v1-040-application-pipeline-ui` | Application pipeline, approval and status UI. |
| V1-051 | `careeros-communication-service` | `story/v1-051-notification-preferences` | Notification preferences, consent, quiet hours, deduplication and digest policy. |
| V1-052 | `careeros-communication-service` | `story/v1-052-notification-channel` | In-app notification history, Telegram account linking and provider-neutral delivery-request contract. |
| V1-053 | `careeros-automation` | `story/v1-053-telegram-notification-workflow` | Credential-free n8n workflow using the Telegram node, with idempotency, retry and delivery-result reporting. |

## Epic 5 — Analytics, hardening and release

### Feature 5.1 — Privacy-conscious analytics

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-041 | `careeros-analytics-service` | `story/v1-041-analytics-scaffold` | Service scaffold and minimized lifecycle-event consumers. |
| V1-042 | `careeros-analytics-service` | `story/v1-042-funnel-aggregates` | Per-user funnel aggregates without raw document content. |
| V1-043 | `careeros-web` | `story/v1-043-analytics-dashboard` | Dashboard for job, resume, application and interview funnel. |

### Feature 5.2 — V1 hardening and release

| Key | Repository | Branch | Deliverable |
| --- | --- | --- | --- |
| V1-044 | `careeros-acceptance-tests` | `story/v1-044-e2e-happy-path` | Repeatable black-box end-to-end test for the complete V1 journey. |
| V1-045 | `careeros-workspace` | `story/v1-045-security-review` | Authorization, tenancy, privacy, secret and audit review. |
| V1-046 | `careeros-infrastructure` | `story/v1-046-backup-restore` | Backup/restore procedure and operational smoke test. |
| V1-047 | `careeros-workspace` | `story/v1-047-v1-release` | Release checklist, changelog, version tags and known limitations. |

## Recommended execution order

1. Complete Epic 0, including the first business-rule catalog and conformance harness, before service implementation.
2. Deliver Epic 1 as the first vertical slice.
3. Deliver job capture and deterministic matching before adding model-powered enrichment.
4. Complete resume generation before ATS validation.
5. Complete application tracking before real communication delivery.
6. Add analytics only after the source lifecycle events are stable.
7. Run hardening and the end-to-end journey before tagging V1.

## Pull request checklist

- Linked central story and owning repository are correct.
- Acceptance criteria are demonstrably satisfied.
- Tests include success, validation and authorization-denial paths.
- No real personal data or secrets are present.
- Public contracts and documentation are updated.
- Logs redact payloads and propagate correlation identifiers.
- PR remains inside the size budget or explains why it cannot be split safely.
- CI is green and the reviewer can reproduce the result locally.
