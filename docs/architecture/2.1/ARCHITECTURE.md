# AI Engineering Standard 2.1 Architecture

## Purpose

Version 2.1 extends the 2.0 engineering standard with a canonical, framework-neutral model for multi-agent work. The architecture defines contracts before runtime implementations so that orchestration frameworks, IDE agents, MCP adapters, and model providers remain replaceable.

## Canonical execution model

```
Work Unit
   │
   ├── Agent + Agent Role
   │        │
   │        └── Agent Contract
   │
   ├── Handoff
   │
   ├── Evidence
   │
   └── Evaluation
           │
           ▼
       Acceptance
```

The unit of standardization is the **Work Unit**, not a chat message, model call, or framework task.

## Canonical boundaries

- **Agent** — an execution identity with declared capabilities and permission ceilings.
- **Agent Role** — a bounded responsibility assigned to an agent for a work unit.
- **Agent Contract** — the executable agreement for inputs, outputs, permissions, and completion obligations.
- **Work Unit** — the smallest independently traceable unit of work with an owner, lifecycle, and acceptance boundary.
- **Handoff** — a typed transfer of responsibility and evidence between agents or roles.
- **Evidence** — immutable or content-addressed material that supports claims about execution.
- **Evaluation** — deterministic or explicitly qualified assessment of evidence against criteria.
- **Acceptance** — the final decision that the work unit satisfies its declared completion criteria.

## Design invariants

1. Contracts are framework-neutral.
2. Every work unit has one canonical identity.
3. Agent permissions cannot exceed the declared role ceiling.
4. Handoffs preserve provenance and identify sender and receiver.
5. Evidence is referenced by identity rather than inferred from logs, and an evidence identity cannot be overwritten by a later record.
6. Evaluation cannot silently upgrade UNTESTED runtime evidence to PASS.
7. Acceptance is downstream of evaluation and cannot manufacture evidence.
8. Retries create a new invocation identity while retaining parent lineage.
9. v2.0 contracts remain valid; v2.1 adds contracts rather than replacing existing evidence and validation rules.
10. Runtime implementations are adapters to these contracts, not sources of canonical semantics.
11. Canonical registry identities are immutable; duplicate Agent, Role, Work Unit, Agent Contract, Handoff, Evaluation, or Evidence IDs are rejected.
12. Work Unit ownership and parent lineage references must resolve to registered canonical identities.
13. Each Work Unit has at most one bound Agent Contract, and its contract agent must be the Work Unit owner.
14. A Work Unit parent reference is immutable after creation; lineage changes require a new canonical Work Unit identity.

## Lifecycle

```
CREATED → READY → EXECUTING → HANDOFF_PENDING → EVALUATING → ACCEPTED
                                      │                 │
                                      └──────────────→ BLOCKED
                                                        │
                                                        ▼
                                                     RETRY
```

Implementations may expose richer internal states, but they must map to the canonical lifecycle before evidence is accepted.

## Multi-agent rule

Parallel agents are allowed only when their work units have explicit ownership and their merge/acceptance boundary is defined. Shared mutable state is not a handoff mechanism.

## Compatibility

Version 2.1 does not mandate a specific model, agent framework, MCP implementation, IDE, scheduler, or message bus. An implementation conforms by producing the canonical contracts and evidence defined here.


## Lifecycle enforcement

The reference runtime enforces the canonical Work Unit lifecycle at operation boundaries. Agent contracts bind only to `CREATED` work units; `start` moves `READY` to `EXECUTING`; handoff requires `EXECUTING` and moves the unit to `HANDOFF_PENDING`; evaluation is allowed from `EXECUTING` or `HANDOFF_PENDING`, records `EVALUATING`, and then maps acceptance to `ACCEPTED`, `REJECTED`, or `BLOCKED`. Completed work units cannot be evaluated again.


## Evidence identity enforcement

The reference runtime treats evidence IDs as immutable provenance identities. Recording evidence for an unknown Work Unit is rejected, and recording a second evidence item with an existing ID is rejected rather than replacing the original evidence. Handoff, retry, and evaluation references therefore remain bound to the original evidence record.


## Canonical identity enforcement

The reference runtime treats every canonical registry ID as an immutable provenance identity. Registration or creation with an existing Agent, Role, Work Unit, Agent Contract, Handoff, Evaluation, or Evidence ID is rejected rather than replacing the original record.

This prevents a later registration from silently changing the entity referenced by an existing contract, handoff, evaluation, retry lineage, or evidence record. Implementations that need a revised entity must create a new canonical identity and preserve the lineage explicitly.


## Work Unit lineage integrity

The reference runtime requires every Work Unit owner to be a registered Agent. Optional parent references must resolve to an existing Work Unit and may not point to the Work Unit itself. Parallel child Work Units may share an existing parent while retaining independent ownership and identity.

This keeps ownership and lineage referentially valid before execution begins; it does not impose scheduler ordering or require a specific parent/child execution strategy. The reference runtime makes `parent_id` immutable after Work Unit creation, so an existing node cannot be reassigned to a descendant and create an indirect cycle.


## Agent Contract binding integrity

The reference runtime requires an Agent Contract to bind to the Work Unit owner and rejects a second contract for a Work Unit. This makes the contract binding a single canonical authorization boundary before execution begins.


## Evaluation actor authorization

The reference runtime authorizes an agent evaluation actor only when the actor is the Work Unit owner or the receiver of a recorded handoff for that Work Unit. A registered agent that has no ownership or handoff provenance cannot manufacture an evaluation outcome. Human actors remain separately authorized by explicit human-approval evidence.
