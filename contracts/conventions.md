# CareerOS contract conventions

These conventions are normative for V1 public service contracts. They cover HTTP APIs, asynchronous events and shared JSON schemas. A service-specific contract may be stricter but must not silently weaken these rules.

## Contract formats and layout

- HTTP APIs use OpenAPI 3.1.2.
- Message-driven APIs use AsyncAPI 3.1.0.
- Reusable payload schemas use JSON Schema 2020-12.
- OpenAPI files live under `contracts/openapi/<service>/v1/`.
- AsyncAPI files live under `contracts/asyncapi/<service>/v1/`.
- Shared schemas live under `contracts/json-schema/<domain>/` and include the major version in the filename and `$id`.

JSON payloads use UTF-8, `camelCase` property names, RFC 3339 UTC timestamps ending in `Z`, and opaque string identifiers. Optional values are absent unless `null` has an explicit domain meaning. Examples use synthetic, non-identifying values only.

The `info.version` of an OpenAPI or AsyncAPI document is the semantic version of that contract document. It is distinct from the public API or event major version.

## HTTP API conventions

### Resource and operation versioning

The public major version appears in the path, for example `/v1/applications`. The following changes are compatible within a major version when their defaults and semantics are documented:

- adding an operation or resource;
- adding an optional request property;
- adding a response property that consumers may ignore;
- adding a new optional header;
- adding an error type without changing an existing error's meaning.

The following changes require a new major version:

- removing or renaming an operation, property or supported value;
- making an optional input required;
- changing a property's type, constraints or meaning;
- changing authorization, ownership or side-effect semantics;
- changing an established success status or error type in a way that alters client behavior;
- adding a value to a closed enum.

Extensible values are modeled as strings with a documented unknown-value fallback, not as closed enums. Consumers must ignore unknown response properties. Removed names are never reused for different meanings.

A deprecated operation is marked `deprecated: true`, documents its successor and migration path, and returns `Deprecation` and `Sunset` headers when a retirement date is known. Breaking versions coexist until identified consumers have migrated; the migration window is recorded in the contract change.

### HTTP semantics and pagination

- `GET` and `HEAD` are safe and idempotent.
- `PUT` and `DELETE` are idempotent according to their resource semantics.
- `POST` operations with retryable or consequential side effects use the idempotency convention below.
- Creation returns `201 Created` with a `Location` header. Accepted asynchronous work returns `202 Accepted` with a status resource location.
- Updates that require optimistic concurrency use `ETag` and `If-Match`; a stale precondition returns `412 Precondition Failed`.

Collections use opaque cursor pagination. Requests use `pageSize` and `cursor`; responses contain `items` and `page.nextCursor`. Contracts define the maximum page size and stable sort order. Offset pagination and total counts are used only when the owning service can provide stable, inexpensive semantics.

### Authentication and authorization

OpenAPI documents declare the configured OpenID Connect security scheme and the scopes required by each operation. Authentication establishes identity; every service still performs authorization, ownership and tenant checks at its own boundary.

- `401 Unauthorized` means credentials are missing, invalid or expired and includes `WWW-Authenticate` where applicable.
- `403 Forbidden` means the authenticated caller is known but lacks permission and revealing resource existence is safe.
- `404 Not Found` is also used for an unowned resource when returning `403` would reveal its existence.

Clients must not infer that an identifier exists from timing, error details or different response shapes.

### Error envelope

All non-success HTTP responses with a body use RFC 9457 Problem Details and `Content-Type: application/problem+json`. CareerOS adds stable `code`, `correlationId` and optional `errors` members:

```json
{
  "type": "urn:careeros:problem:validation-failed",
  "title": "Request validation failed",
  "status": 422,
  "detail": "One or more fields are invalid.",
  "instance": "urn:uuid:018f7f2c-50d7-7c18-b3a9-52f260ad6d3f",
  "code": "VALIDATION_FAILED",
  "correlationId": "018f7f2c-365b-7a19-9b42-189dd4a10e61",
  "errors": [
    {
      "pointer": "/title",
      "code": "REQUIRED",
      "message": "A title is required."
    }
  ]
}
```

- `type` is a stable URI identifying the problem class.
- `title` is a stable, human-readable summary for that type.
- `status` matches the HTTP response status.
- `detail` helps correct the request but is not machine-parsed.
- `instance` identifies this occurrence without exposing an internal path or record.
- `code` is a stable uppercase machine code.
- `correlationId` matches the response `X-Correlation-ID` header.
- `errors[].pointer` is a JSON Pointer into the request when a field is involved.
- `errors[].code` is stable; `errors[].message` is safe display text.

Services use these status classes consistently:

| Status | Meaning |
| --- | --- |
| `400` | Malformed JSON, header, query or path syntax. |
| `401` | Missing, invalid or expired authentication. |
| `403` | Authenticated caller lacks permission and disclosure is safe. |
| `404` | Resource is absent or its existence is concealed. |
| `409` | State conflict, idempotency conflict or operation already in progress. |
| `412` | Optimistic-concurrency precondition failed. |
| `422` | Syntactically valid request violates declared validation or domain constraints. |
| `429` | Rate limit exceeded; include `Retry-After`. |
| `500` | Unexpected internal failure with no implementation detail. |
| `502`/`503` | Upstream or temporary service failure; include `Retry-After` when known. |

Errors never contain stack traces, SQL, provider payloads, tokens, secrets, raw resumes, application content or personal data. Provider-specific failures are mapped to a documented CareerOS problem type.

### Idempotency

`Idempotency-Key` is required for `POST` operations that may be retried or create a consequential side effect, including document generation, application submission and external delivery. Each OpenAPI operation explicitly declares whether the header is required and its retention window.

The key is an opaque 16-128 character value using letters, digits, `.`, `_`, `:`, or `-`. It contains no user or resource data. Its scope is the authenticated actor, operation and service.

For a given scope and key, the service stores a fingerprint of the effective request and the final outcome:

1. The first request executes once and records its status, safe response body and relevant response headers.
2. The same key and same effective request returns the recorded outcome without repeating the side effect and adds `Idempotency-Replayed: true`.
3. The same key with a different effective request returns `409` with code `IDEMPOTENCY_KEY_REUSED`.
4. A concurrent duplicate while the first request is unfinished returns `409` with code `IDEMPOTENCY_IN_PROGRESS` and `Retry-After`, unless the operation contract promises to wait and replay.
5. A missing or malformed required key returns `400` without executing the operation.

The normal minimum retention is 24 hours. Keys for external messages, submissions or other audited side effects are retained with the owning audit record so a retry cannot silently repeat the action. Services must make persistence of the side effect and its idempotency outcome atomic or recoverable. Provider idempotency keys are used when available, but the provider never replaces CareerOS's own record.

An idempotency key is not a correlation identifier, authorization proof or event identifier.

Idempotency never replaces explicit action-time approval. Contracts for external submissions and deliveries require an immutable approval reference, revalidate that approval immediately before the side effect, and preserve the meaning of `BR-APP-004` and `BR-COM-001` through `BR-COM-003`.

### Correlation and trace context

Every HTTP request has an `X-Correlation-ID`. A service accepts a single valid UUID from a trusted upstream; otherwise it generates a new value. The value is returned in the response and propagated to downstream calls and resulting events.

Distributed tracing uses W3C `traceparent` and `tracestate`. Services validate incoming trace context, create or update the current span, and propagate the resulting context. Correlation and trace values contain no user, tenant, email or resource data and never affect authorization decisions.

Structured logs include the correlation ID and, when available, trace ID, operation, service and safe outcome code. They exclude request and response bodies by default.

## Asynchronous event conventions

### Event envelope and naming

Events are completed facts named in the past tense and use CloudEvents 1.0.2 structured JSON. Commands are modeled separately and must not masquerade as facts.

```json
{
  "specversion": "1.0",
  "id": "018f7f2c-7011-76b4-b64a-5fb8813aa0af",
  "source": "urn:careeros:application-service",
  "type": "com.careeros.application.approved.v1",
  "subject": "applications/app_demo_123",
  "time": "2026-11-22T15:30:00Z",
  "datacontenttype": "application/json",
  "dataschema": "urn:careeros:schema:application-approved:v1",
  "correlationid": "018f7f2c-365b-7a19-9b42-189dd4a10e61",
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
  "data": {
    "applicationId": "app_demo_123",
    "approvalId": "approval_demo_456"
  }
}
```

- `id` is globally unique and stable across redelivery.
- `source` identifies the owning producer service.
- `type` follows `com.careeros.<domain>.<fact>.v<major>`.
- `subject` is the opaque aggregate reference used for partitioning or ordering when needed.
- `time` records when the fact occurred, not when a retry published it.
- `dataschema` identifies the versioned `data` schema.
- `correlationid` carries the initiating workflow correlation ID.
- `traceparent` carries W3C trace context when available.

RabbitMQ messages use persistent delivery, set AMQP `message_id` to the CloudEvent `id`, set `correlation_id` to `correlationid`, and use `application/cloudevents+json` as the content type. Payloads contain only stable identifiers and the minimum context consumers need; large or sensitive artifacts are referenced through authorized service APIs.

Each AsyncAPI channel identifies its producer, known consumers, data owner, routing key and an `x-careeros-delivery` extension containing delivery guarantee, maximum attempts, backoff policy, dead-letter destination and ordering scope.

### Event compatibility

Adding an optional `data` property is compatible only when consumers ignore unknown properties and the absence of the new property preserves meaning. Removing, renaming, changing meaning, making a property required or adding a closed-enum value is breaking.

A breaking event change creates a new event type and schema major version. Producers publish both versions during a documented migration window when consumers cannot move atomically. Old production stops only after every registered consumer has been verified on the new type. An event type is never reused for a different fact.

### Delivery, ordering and replay

Delivery is at least once. Each consumer records processed event IDs or derives an equally stable idempotency key before producing side effects. Duplicate delivery returns a successful acknowledgement without repeating work.

Global ordering is not guaranteed. When order matters, the event contract declares ordering by `subject` and includes a monotonic domain sequence in `data`. Consumers detect stale events and gaps and must not guess missing state.

Only transient failures are retried. Schema failures, unsupported versions and permanent authorization failures go directly to the declared dead-letter destination with safe failure metadata. Exhausted retries also dead-letter the original envelope. Replay is explicit, authorized and audited; dead-letter consumers never create an automatic infinite loop.

When database state and event publication represent one fact, producers use a transactional outbox or an equivalent recoverable mechanism. Consumers validate the envelope and the versioned data schema before domain processing.

## Contract change workflow and evidence

The workspace contract changes before or with an implementation. Every change identifies affected producers, consumers, authorization boundaries and migration order. Prefer additive producer changes, then consumer rollout, then removal only in a new major version.

Each implemented HTTP operation provides automated contract evidence for:

- the documented success response;
- malformed input and semantic validation failure;
- missing authentication and denied authorization or ownership;
- idempotent replay and conflicting key use when applicable;
- unknown response fields remaining safe for tolerant consumers.

Each implemented event provides automated evidence for:

- producer output matching the envelope and data schema;
- consumer handling of valid data and compatible optional fields;
- duplicate and out-of-order delivery;
- retry exhaustion, dead-letter routing and authorized replay when applicable;
- rejection of invalid or unsupported schema versions without unsafe side effects.

V1-008 adds repository-wide schema linting and compatibility gates. Until then, reviewers verify these conventions and the service-local contract tests. This document changes integration conventions only; it does not add or change a CareerOS business rule.

## References

- [OpenAPI Specification 3.1.2](https://spec.openapis.org/oas/v3.1.2)
- [AsyncAPI Specification 3.1.0](https://www.asyncapi.com/docs/reference/specification/v3.1.0)
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12)
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [CloudEvents 1.0.2](https://github.com/cloudevents/spec/tree/v1.0.2)
- [IETF Idempotency-Key draft](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
