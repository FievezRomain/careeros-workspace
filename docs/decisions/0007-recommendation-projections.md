# ADR 0007: Versioned recommendation projections and outbox

Status: proposed for V1-058.

The matching service owns durable recommendation evaluations, transitions,
extraction evidence and notification intent in its PostgreSQL database. Job and
profile services own their source versions. A trusted, account-bound projector
maps source events and owned API responses to versioned matching HTTP updates.
The projection carries confirmed facts, decision criteria and verified source
requirements. Opportunity and profile projections can arrive in either order.

The match identity combines the immutable job, confirmed profile and criteria
versions with the matcher version. A user correction has its own evidence
revision. One successful extraction can serve multiple profiles in the same
tenant when they share the same immutable opportunity version and source.

The matching transaction records evidence, the latest decision, the event receipt
and the outgoing intent atomically. `com.careeros.recommendation.created.v1` is a
CloudEvent for an inactive-to-active transition. A deployment relay reads the
owned outbox and forwards that event on `recommendation.created.v1`. Delivery is
at least once and downstream consumers deduplicate by event ID. Channel delivery
and preference checks are owned by the notification workflow.
