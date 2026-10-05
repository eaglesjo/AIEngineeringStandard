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
5. Evidence is referenced by identity rather than inferred from logs.
6. Evaluation cannot silently upgrade UNTESTED runtime evidence to PASS.
7. Acceptance is downstream of evaluation and cannot manufacture evidence.
8. Retries create a new invocation identity while retaining parent lineage.
9. v2.0 contracts remain valid; v2.1 adds contracts rather than replacing existing evidence and validation rules.
10. Runtime implementations are adapters to these contracts, not sources of canonical semantics.

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
