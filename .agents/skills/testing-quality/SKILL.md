---
name: testing-quality
description: Define or review CareerOS test strategy, CI gates, contract tests, security checks and release evidence across services.
---

# Testing and quality

- Cover domain rules with unit tests and boundaries with integration tests.
- Add contract tests for APIs and events and regression tests for fixed failures.
- Use synthetic fixtures only and scan commits for secrets.
- Keep tests deterministic; isolate provider calls behind fakes or controlled sandboxes.
- Report what was verified, what was not, and any remaining operational risk.