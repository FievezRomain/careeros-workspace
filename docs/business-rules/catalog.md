# CareerOS functional business-rule catalog

Status: V1 baseline. This document contains functional rules only. Technical design and deployment are deliberately excluded.

## Accounts and user control

| ID | Business rule |
| --- | --- |
| BR-ACC-001 | A person must be signed in before accessing their CareerOS workspace. |
| BR-ACC-002 | A person can see and change only their own profile, opportunities, resumes, applications, messages and results. |
| BR-ACC-003 | A person can request an export of the information they supplied and the career artifacts created for them. |
| BR-ACC-004 | A person can request deletion of their CareerOS account; the product explains what is deleted immediately and what must be retained for a stated legal or audit reason. |
| BR-ACC-005 | A person must explicitly choose whether optional communication channels may be used. Refusing an optional channel cannot block the core product. |

## Professional profile and evidence

| ID | Business rule |
| --- | --- |
| BR-PRO-001 | A profile can contain identity details, contact details, target roles, locations, work preferences, experiences, education, skills, languages and certifications. |
| BR-PRO-002 | A profile fact is either user-confirmed or unconfirmed; generated text never becomes a confirmed fact without the person's approval. |
| BR-PRO-003 | Every material profile fact records its origin, such as direct entry, imported resume or later user correction. |
| BR-PRO-004 | End dates cannot precede start dates, and an item marked current has no past end date. |
| BR-PRO-005 | A skill may include a self-declared level and supporting experiences, but CareerOS must not present a self-declaration as an independent certification. |
| BR-PRO-006 | Removing or correcting a profile fact does not silently rewrite resumes or applications that were already approved; those artifacts retain the snapshot used to create them. |
| BR-PRO-007 | Before generating an application artifact, CareerOS identifies missing facts required for that artifact and asks for confirmation instead of inventing them. |
| BR-PRO-008 | A person can activate, pause and resume an owned automatic opportunity search with explicit criteria, timezone and daily search window; every material criteria change creates an immutable version. |
| BR-PRO-009 | Role, skill, experience, location, work-preference and search-criteria changes request rematching, while contact-only and presentation-only changes do not. |
| BR-PRO-010 | Opportunity retrieval receives only a minimum provider-neutral search signature and may be shared only for exactly equivalent normalized search dimensions; individual criteria are never averaged or weakened. |

## Job opportunities

| ID | Business rule |
| --- | --- |
| BR-JOB-001 | A person can record an opportunity manually from a title, employer, description and source reference. |
| BR-JOB-002 | A detected opportunity records where and when it was found and preserves the source wording needed to understand the result. |
| BR-JOB-003 | Repeated discoveries of the same role from the same employer are grouped when they represent the same opportunity; the person can separate them if the grouping is wrong. |
| BR-JOB-004 | A materially changed source creates a new opportunity version and does not silently overwrite the version used by an existing application. |
| BR-JOB-005 | An opportunity can be marked saved, ignored, expired or converted into an application. Ignored and expired opportunities are excluded from active recommendations. |
| BR-JOB-006 | CareerOS must distinguish information stated by the source from information inferred or left unknown. |
| BR-JOB-007 | A newly detected opportunity is notified only when it is not a duplicate, is still actionable and meets the person's saved criteria or notification threshold. |

## Matching and recommendations

| ID | Business rule |
| --- | --- |
| BR-MAT-001 | A match compares one version of an opportunity with one confirmed profile snapshot. |
| BR-MAT-002 | A match result identifies satisfied, partially satisfied, missing and unknown requirements. |
| BR-MAT-003 | Every positive or negative finding is supported by an opportunity statement and, when applicable, a confirmed profile fact. |
| BR-MAT-004 | Unknown information is not treated as either satisfied or missing. |
| BR-MAT-005 | Mandatory requirements weigh more than optional preferences, and a hard eligibility conflict is shown separately from the overall score. |
| BR-MAT-006 | A score is an aid to prioritization, not a promise of interview or employment. The interface must state this limitation. |
| BR-MAT-007 | The person can correct an incorrectly extracted requirement; a correction produces a new result without rewriting the earlier result. |
| BR-MAT-008 | Recommendations are ordered using the person's current criteria, but the person can inspect why each opportunity was included or excluded. |

## Resume and application documents

| ID | Business rule |
| --- | --- |
| BR-RES-001 | A generated resume may use only confirmed facts from the selected profile snapshot. |
| BR-RES-002 | CareerOS may rephrase a confirmed fact but must not invent an employer, title, date, result, metric, skill, certification or responsibility. |
| BR-RES-003 | A generated resume identifies the opportunity and profile snapshot used to create it. |
| BR-RES-004 | The person reviews and explicitly approves a resume version before it can be included in an external application. |
| BR-RES-005 | Editing a generated resume creates a new version and preserves the previously approved version. |
| BR-RES-006 | A resume cannot be presented as current when a referenced profile fact was later withdrawn or corrected; CareerOS warns the person and offers regeneration. |
| BR-RES-007 | Exported documents must not contain internal scores, hidden prompts, internal comments or unrelated personal information. |

## ATS assessment

| ID | Business rule |
| --- | --- |
| BR-ATS-001 | An ATS assessment applies to the final exported document, not merely to its editable draft. |
| BR-ATS-002 | Structural findings and relevance findings are reported separately. |
| BR-ATS-003 | Every finding identifies the affected content, the rule applied and a concrete correction when one is available. |
| BR-ATS-004 | A technical score reflects only the published CareerOS checks and is never described as the score of a named employer's ATS. |
| BR-ATS-005 | Missing or unreadable content produces an explicit inconclusive result rather than a passing score. |
| BR-ATS-006 | Regenerating or editing a document invalidates the previous assessment for the new version. |
| BR-ATS-007 | CareerOS never guarantees that a document will pass every recruitment system or lead to an interview. |

## Applications and lifecycle

| ID | Business rule |
| --- | --- |
| BR-APP-001 | An opportunity has at most one active application per person unless the person explicitly confirms that separate applications are intended. |
| BR-APP-002 | An application follows the states draft, ready for approval, submitted, acknowledged, interview, offer, rejected, withdrawn or archived. |
| BR-APP-003 | A transition records when it happened, who or what reported it and any user-visible note. |
| BR-APP-004 | A submitted state requires either an explicit user confirmation or a supported provider confirmation; preparing documents alone never means submitted. |
| BR-APP-005 | Rejected, withdrawn and archived are terminal for the current application; reopening creates an explicit new active phase. |
| BR-APP-006 | An interview may contain several stages, dates and contacts without losing the application's overall interview state. |
| BR-APP-007 | An offer records the date received and the person's decision separately; an offer is not automatically accepted. |
| BR-APP-008 | A meaningful externally reported status change is shown to the person and can trigger a notification according to their preferences. |
| BR-APP-009 | A person can correct a wrong status while preserving that a correction occurred. |

## Messages, follow-ups and notifications

| ID | Business rule |
| --- | --- |
| BR-COM-001 | CareerOS may prepare a message draft, but the person must preview and approve its content, recipients and channel before external delivery. |
| BR-COM-002 | Approval applies to one concrete message version and cannot be reused after the content, recipient or attachment changes. |
| BR-COM-003 | A repeated delivery request for the same approved message must not send a duplicate. |
| BR-COM-004 | A failed delivery remains distinguishable from a delivered message and tells the person whether retrying is safe. |
| BR-COM-005 | A follow-up becomes due from the last meaningful application activity and the person's chosen delay; it is cancelled when the application reaches a terminal state. |
| BR-COM-006 | A due follow-up creates a draft or reminder, never an unapproved external message. |
| BR-COM-007 | The person can enable or disable each notification category and delivery channel independently. |
| BR-COM-008 | In-app history and Telegram Bot delivery are the V1 notification channels. Email is not used. Telegram delivery starts only after explicit opt-in and successful account linking. |
| BR-COM-009 | Equivalent events occurring close together are grouped so that the person is not notified repeatedly about the same change. |
| BR-COM-010 | Quiet hours defer non-urgent notifications until the next allowed period; CareerOS has no V1 event that overrides quiet hours as an emergency. |
| BR-COM-011 | A notification states why it was sent and provides a direct way to view the related opportunity or application. |
| BR-COM-012 | Disabling a channel stops future sends through that channel without deleting the underlying opportunities, applications or in-app history. |
| BR-COM-013 | Provider fees, unavailable channels or provider rejection must not cause a silent loss: the notification remains visible in-app and its external delivery state is shown. |
| BR-COM-014 | Telegram linking begins only after the person starts the CareerOS bot and confirms a one-time association from their signed-in CareerOS account; the person can revoke the association at any time. |
| BR-COM-015 | An external notification contains only the minimum information needed to understand the event and a link back to CareerOS; resume content, message bodies and private application notes are not sent in the notification. |

## Analytics and progress insights

| ID | Business rule |
| --- | --- |
| BR-ANA-001 | Progress counts are derived from lifecycle events and use published definitions for detected, saved, applied, interviewed, offered and accepted. |
| BR-ANA-002 | A missing value is shown as unavailable, never silently replaced by zero. |
| BR-ANA-003 | Conversion rates state their numerator, denominator and period. A rate is unavailable when its denominator is zero. |
| BR-ANA-004 | One application contributes at most once to a given lifecycle milestone, even if that milestone is reported repeatedly. |
| BR-ANA-005 | Correcting an application state corrects future analytics while preserving that the earlier observation existed. |
| BR-ANA-006 | Analytics never expose resume text, message bodies or another person's data. |
| BR-ANA-007 | Insights explain their scope and cannot be presented as a hiring probability or employment guarantee. |

## Generated suggestions and human decisions

| ID | Business rule |
| --- | --- |
| BR-AI-001 | Generated suggestions are visibly identified as suggestions until accepted by the person. |
| BR-AI-002 | A generated result that lacks required evidence is rejected or marked inconclusive rather than treated as a fact. |
| BR-AI-003 | Changing the generation provider must not change the business meaning of approvals, ownership, evidence or application states. |
| BR-AI-004 | The person can reject a suggestion without changing the confirmed facts that produced it. |
| BR-AI-005 | CareerOS does not make irreversible career decisions, submit applications or contact third parties solely from a generated recommendation. |

## Rule evolution

| ID | Business rule |
| --- | --- |
| BR-GOV-001 | A user story that changes observable product behavior names every business rule it adds, changes or deprecates. |
| BR-GOV-002 | A changed business meaning receives a new rule identifier; the former rule remains traceable as deprecated. |
| BR-GOV-003 | A V1 rule is considered regression-protected when an executable acceptance scenario references it, unless the catalog explicitly records a justified manual check. |
