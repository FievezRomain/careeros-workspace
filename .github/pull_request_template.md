## Central story

Link the `careeros-workspace` user story and use `Closes FievezRomain/careeros-workspace#<number>` when this PR completes it.

## Outcome

Describe the user-visible or architectural outcome, not only the implementation.

## Scope

- Included:
- Explicitly excluded:

## Verification

- [ ] Acceptance criteria are covered.
- [ ] Success, validation and authorization-denial paths are tested.
- [ ] Public contracts and documentation are updated when affected.
- [ ] Business behavior is unchanged, or `docs/business-rules/catalog.md` is updated with stable `BR-...` identifiers.
- [ ] Every added or changed business rule has an executable scenario in `careeros-acceptance-tests`.
- [ ] The `acceptance-tests` submodule points to the tested acceptance commit and `coverage:no-new-gaps` passes.
- [ ] No secret, real CV, real application or personal data is included.
- [ ] Logs redact payloads and preserve correlation identifiers.
- [ ] CI is green and local verification steps are documented.
- [ ] Python service changes pass the executable service baseline and every command declared in `[tool.careeros.quality]`.
- [ ] Judgment-based findings were reviewed with `code-quality-review` (P0-P3), plus the relevant domain/security skill.
- [ ] Hexagonal dependencies point inward; boundary DTOs, messages and settings use Pydantic v2.

## PR budget

- Hand-edited files:
- Changed lines excluding lockfiles/generated artifacts:
- Database migrations:

- [ ] At most 8 hand-edited files.
- [ ] At most 400 changed lines excluding lockfiles/generated artifacts.
- [ ] At most one migration.
- [ ] If a limit is exceeded, the reason this cannot be split safely is documented above.

