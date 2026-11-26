# ADR 0006: Open-web job discovery evidence

Status: proposed for V1-057.

The AI gateway owns bounded query expansion, retrieval provider configuration,
validation and a short query cache. The job service owns canonical verification,
external link retention, deduplication, versioning and catalog evidence.

Job discovery invokes `discover-job-links` schema `1.0` through the existing
gateway invocation endpoint with `ai:invoke`. `input` contains `targetRoles`,
`locations`, `remotePolicy` and `contractTypes`. `output.results` contains `url`,
`title`, `snippet`, `score` and `source`. `output.searchRequests` counts logical
queries. The gateway never receives private criteria, identifiers or profile facts.

The job service verifies explicitly referenced Greenhouse jobs using its public
Job Board API. Other search results remain link-only and carry source uncertainty.
The catalog exposes `sourceAccess`, `resumeEligible` and `evidence.unknownFields`.
For link-only records, unavailable description, employer and location are null.
Consumers should roll out support for that variant before enabling the optional
web source. Existing discovery events still reference the owning catalog version.

Matching consumes the evidence state under V1-058. Resume generation uses the
catalog eligibility under V1-059. The gateway and catalog do not read each
other's databases or credentials. BR-JOB-002, BR-JOB-003, BR-JOB-004,
BR-JOB-006 and BR-AI-002 have dedicated HTTP acceptance scenarios.
