# v2.1 Handoff Provenance Conformance

A handoff is a canonical transfer boundary, not an informational log entry.

## Required provenance

A valid handoff identifies:

- the Work Unit;
- a registered sender agent;
- a registered receiver agent;
- the sender's authorized Agent Contract for that Work Unit;
- the Work Unit owner;
- a non-empty payload reference;
- a non-empty reason;
- evidence references belonging to the same Work Unit;
- a timestamp.

The reference runtime rejects:

- unknown sender agents;
- unknown receiver agents;
- senders without an authorized contract for the Work Unit;
- senders that do not own the Work Unit;
- empty reasons or payload references;
- evidence belonging to another Work Unit.

This makes sender, receiver, payload, and evidence provenance explicit and auditable.

## Non-goals

The conformance does not define network transport, queue semantics, delivery guarantees, or a particular agent framework.
