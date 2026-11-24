# careeros-automation

Credential-free exported workflows and approval gates.

Repository: https://github.com/FievezRomain/careeros-automation

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.

## V1-056 daily discovery

- `v1-056-profile-search-projection.json` consumes
  `profile.match-relevant-change.v1`, validates schema `1.0` and forwards only
  the minimum schedule and signature projection to the job service. The broker
  message is acknowledged only after successful processing.
- `v1-056-daily-opportunity-discovery.json` wakes every 15 minutes. The job
  service remains responsible for timezone windows, once-per-local-day
  selection and exact-signature retrieval sharing.
- Each UTC bucket uses one stable idempotency key and correlation identifier.
  Four attempts reuse that key with 30, 120 and 480 second backoffs; exhaustion
  publishes a minimal record to `careeros.discovery.run.v1.dlq`.
- Exports contain no credentials. The runtime injects
  `CAREEROS_AUTOMATION_TOKEN`, and RabbitMQ uses the externally configured
  `CAREEROS_RABBITMQ` credential.
- Execution payload persistence is disabled for the scheduled flow. Dead-letter
  records contain only schema version, idempotency key, correlation ID, attempt
  count, failure time and HTTP status.
- Generic scraping, CAPTCHA or protection bypass, application submission and
  notification delivery are outside these workflows.

Import order, broker policies and replay recovery are maintained in the
automation repository's `docs/v1-056-runbook.md`.
