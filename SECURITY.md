# Security Policy

CareerOS is developed in public, but personal data and secrets are never public artifacts.

## Reporting a vulnerability

Do not open a public issue containing exploitable details. Use GitHub private vulnerability reporting when available, or contact the maintainer through a private channel.

## Repository rules

- Never commit tokens, passwords, OAuth credentials, private keys, real CVs, real applications or personal contact data.
- Use environment variables or a dedicated secret store. Public examples contain placeholders only.
- Keep GitHub Actions permissions minimal and review third-party actions before use.
- Use fictitious, non-identifying fixtures in tests and documentation.
- Revoke and rotate any credential immediately if exposure is suspected.