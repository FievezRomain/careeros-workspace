# careeros-analytics-service

Privacy-conscious aggregates and operational metrics.

Repository: https://github.com/FievezRomain/careeros-analytics-service

Example: derive a privacy-conscious funnel from lifecycle events, such as 42 jobs analyzed, 12 shortlisted, 5 resumes validated, 3 applications submitted and 1 interview, without copying raw CV or application content.

## Shared rules

- Version all public contracts.
- Validate authorization and ownership at the boundary.
- Use fictitious examples only.
- Propagate correlation IDs while redacting sensitive payloads.
- Require explicit user approval for consequential external actions.
