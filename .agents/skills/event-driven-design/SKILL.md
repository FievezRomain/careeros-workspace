---
name: event-driven-design
description: Design CareerOS asynchronous events, queues and consumers with delivery, retry, ordering, idempotency and observability considerations.
---

# Event-driven design

- Events describe completed facts and include schema version, event ID, timestamp and correlation ID.
- Consumers must tolerate duplicates and out-of-order delivery where applicable.
- Define retry limits, dead-letter handling and replay safety.
- Avoid sensitive payloads; publish stable identifiers and minimum necessary context.
- Document producer, consumers, ownership and compatibility expectations.