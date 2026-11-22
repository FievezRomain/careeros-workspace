# CareerOS business rules

This directory contains the functional source of truth for CareerOS. It describes what the product must do from the user's and business's point of view. Architecture, storage, deployment and implementation choices belong elsewhere.

## Canonical document

- [Business-rule catalog](catalog.md)

Every rule has a stable `BR-<DOMAIN>-NNN` identifier. The wording can be clarified without changing the identifier while its business meaning remains the same. A meaning change creates a new rule and deprecates the old one.

## Traceability

Each user story names the rules it implements. Each executable acceptance scenario in `careeros-acceptance-tests` names at least one rule it verifies. A rule is considered protected against regression only when the traceability report finds an active scenario for it, or the catalog explicitly states why it cannot be automated.

The catalog never contains personal data, real resumes, real applications or provider credentials. Examples use fictitious values.
