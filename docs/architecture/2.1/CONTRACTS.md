# AI Engineering Standard 2.1 Canonical Contracts

All identifiers are stable within a repository execution trace. Contract documents use JSON Schema Draft 2020-12.

## Agent

An Agent identifies the execution principal. It declares capabilities but does not itself define the responsibility for a particular work unit.

Required identity:
- `id`
- `name`
- `capabilities`
- `permission_ceiling`

## Agent Role

A Role binds responsibility to a work unit. A role may be fulfilled by different agents.

Required identity:
- `id`
- `name`
- `responsibilities`
- `allowed_permissions`

The effective permission set is the intersection of agent capabilities and role permissions.

## Agent Contract

The Agent Contract binds an agent and role to a specific work unit. It declares:
- input contract;
- output contract;
- effective permissions;
- completion criteria;
- evidence requirements.

An agent contract cannot grant permissions that are absent from either the agent capability set or role ceiling. The contract agent must be the Work Unit owner, and a Work Unit has one active Agent Contract binding.

## Work Unit

A Work Unit is the canonical trace boundary.

It contains:
- a stable identifier;
- objective;
- owner;
- lifecycle status;
- input references;
- output references;
- acceptance criteria.

A Work Unit may contain child work units, but child work must retain parent lineage. The Work Unit `parent_id` is immutable after creation; lineage changes require a new Work Unit identity rather than rewriting an existing parent reference.

## Handoff

A Handoff transfers responsibility or a result between agents/roles.

A valid handoff contains:
- sender and receiver;
- source work unit;
- payload reference;
- evidence references;
- transfer reason;
- timestamp.

A handoff is not equivalent to an arbitrary chat message.

## Evidence

Evidence is a verifiable artifact or observation.

Evidence must identify:
- source;
- type;
- digest or stable reference;
- collection method;
- trust level.

Logs may be evidence only when they satisfy the evidence contract. A log is not evidence merely because it exists.

## Evaluation and Acceptance

Evaluation applies declared criteria to evidence and produces a qualified result.

Allowed results:
- `PASS`
- `PARTIAL`
- `UNTESTED`
- `BLOCKED`
- `FAIL`

Acceptance is a separate decision inside the evaluation contract. It may be:
- `ACCEPTED`
- `REJECTED`
- `INCOMPLETE`

Acceptance cannot be `ACCEPTED` when a required evaluation is `FAIL`, `UNTESTED`, or `BLOCKED`.

Agent evaluation actors must be authorized by Work Unit provenance: the actor is either the Work Unit owner or a receiver recorded in a handoff for that Work Unit. Registration alone does not authorize evaluation.
