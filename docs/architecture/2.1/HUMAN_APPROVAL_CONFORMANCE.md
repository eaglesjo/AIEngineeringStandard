# v2.1 Human Approval Conformance

Human intervention that changes an evaluation outcome must be explicit and auditable.

## Contract

An Evaluation identifies its actor as either:

- an agent; or
- a human.

A human actor may not be represented as an agent identity. When a human actor accepts a Work Unit, at least one referenced Evidence item must have:

- type = human-approval;
- source equal to the evaluation actor identity.

This prevents acceptance from being inferred from an untracked human action.

## Scenario

The conformance fixture demonstrates:

1. an agent produces test evidence;
2. a human approval evidence item is recorded;
3. the Evaluation identifies the human actor;
4. the Evaluation reaches PASS → ACCEPTED;
5. the acceptance retains the human actor and approval evidence provenance.

The reference runtime also rejects ACCEPTED evaluations whose result is not PASS.

This is a deterministic contract fixture, not a UI or identity-provider implementation.
