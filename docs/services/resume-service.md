# careeros-resume-service

Versioned PDF/DOCX generation from verified facts.

Repository: https://github.com/FievezRomain/careeros-resume-service

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.

## V1 resume version registry

The service owns immutable resume version history in its PostgreSQL database.
Each version pins its profile snapshot, optional opportunity version and the
format, opaque object key, byte size and SHA-256 of the declared artifacts.

- `POST /v1/resumes/{resume_id}/versions` registers a version with
  `resume:versions:write` and a UUID `Idempotency-Key`. Repeating the same
  registration returns the original version, while conflicting reuse returns 409.
- `GET /v1/resumes/{resume_id}/versions` paginates owned history in version
  order. `GET /v1/resumes/{resume_id}/versions/{number}` reads an owned version.
  Both require `resume:versions:read`; missing and differently owned records
  return 404.
- The service applies and verifies the owned database migration before readiness.
  Artifact rendering, object storage access and external-use approval are
  separate capabilities.
