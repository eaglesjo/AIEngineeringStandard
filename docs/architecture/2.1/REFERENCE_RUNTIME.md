# v2.1 Reference Runtime

The reference runtime in `core/runtime/v2_1/` makes the canonical multi-agent semantics executable without binding the standard to an LLM provider, orchestration framework, MCP implementation, or IDE.

It demonstrates:

```
Agent + Role → Agent Contract → Work Unit → Evidence → Handoff → Evaluation → Acceptance
```

Effective permissions are the intersection of the registered agent permission ceiling and the role's allowed permissions. Handoffs and evaluations may reference only registered evidence. Retry creates a new attempt with `parent_id`, preserving failed provenance.

This is a deterministic conformance runtime, not a production scheduler.
