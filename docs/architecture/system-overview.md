# CareerOS system overview

CareerOS helps a user manage a job search while keeping the user in control of every consequential external action.

## Primary flow

1. Identity authenticates the user and establishes authorization context.
2. Profile stores verified professional facts and preferences.
3. Job ingests and normalizes opportunities with provenance.
4. Matching produces explainable rankings from versioned profile and job snapshots.
5. Resume generates a tailored document using verified facts only.
6. ATS validates the final PDF/DOCX artifact and produces a versioned report.
7. Application creates a draft and requires explicit approval before submission.
8. Communication prepares messages and follow-ups and requires approval before delivery.
9. Analytics aggregates privacy-conscious operational metrics.

## Boundaries

- Each service owns its data and exposes versioned contracts.
- The AI gateway centralizes provider policy, redaction, quotas, audit metadata and fallbacks.
- Automation coordinates repeatable workflows but never embeds provider credentials in exported definitions.
- Infrastructure contains deployable configuration with placeholders, not environment secrets.

## Trust model

Profile facts, source provenance and user approvals are authoritative. Model output, scraped text, uploaded documents and provider responses are untrusted inputs that must be validated and bounded.