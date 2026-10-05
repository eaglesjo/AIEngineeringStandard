# AI Engineering Standard 2.1 Multi-Agent Model

## Responsibility model

The standard separates identity, responsibility, work, transfer, evidence, and decision.

```
Agent
  ↓ fulfills
Agent Role
  ↓ binds
Agent Contract
  ↓ executes
Work Unit
  ↓ may transfer through
Handoff
  ↓ produces/references
Evidence
  ↓ is assessed by
Evaluation
  ↓ determines
Acceptance
```

## Ownership

Every Work Unit has exactly one canonical owner at a time. Delegation does not remove lineage from the parent work unit.

An orchestrator may assign work, but it is not automatically the owner of every child work unit.

## Parallelism

Parallel work is modeled as separate Work Units or child Work Units. Each unit has:
- independent identity;
- explicit owner;
- declared inputs;
- evidence boundary;
- acceptance criteria.

Joining parallel work requires an explicit evaluation/acceptance boundary.

## Retry and recovery

A retry is a new invocation or Work Unit attempt. It must retain:
- `parent_id`;
- failure evidence;
- reason for retry;
- newly produced evidence.

A retry must not overwrite the provenance of the failed attempt.

## Permissions

Permissions are least-privilege capabilities. Recommended canonical permission atoms are:
- `read`
- `write`
- `execute`
- `web`
- `runtime_observe`

Implementations may define additional permissions, but role ceilings remain mandatory.

## Human intervention

Human approval is modeled as an evaluation/acceptance actor, not as an implicit side effect. Human intervention must be represented in evidence when it changes the work outcome.

## Runtime adapters

A runtime adapter maps its native concepts into the canonical contracts. The adapter may maintain internal queues, messages, memory, tools, and scheduling state, but those details do not redefine the standard.
