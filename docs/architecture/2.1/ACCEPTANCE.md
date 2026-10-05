# AI Engineering Standard 2.1 Acceptance

## Acceptance gate

A v2.1 implementation is acceptable only when:

1. all canonical contract schemas are present and valid;
2. a Work Unit can be traced from creation through evaluation;
3. every handoff identifies sender, receiver, work unit, and evidence;
4. permission ceilings are enforced;
5. retry lineage is preserved;
6. required evidence has an explicit provenance identity;
7. evaluation results distinguish PASS from UNTESTED/BLOCKED;
8. acceptance is derived from evaluation rather than asserted independently;
9. the implementation does not require a specific orchestration framework;
10. all existing v2.0 validation gates remain green.

## Minimum conformance scenario

A reference implementation must demonstrate:

```
create work unit
→ assign role
→ execute agent contract
→ produce evidence
→ handoff to reviewer
→ evaluate evidence
→ accept or reject
```

A second scenario must demonstrate failure and retry without losing the failed attempt's provenance.

## Non-goals

v2.1 does not require:
- a production multi-agent scheduler;
- live LLM execution;
- a specific MCP server;
- a specific IDE;
- cloud infrastructure.

Those are implementation concerns. The standard defines the contract and evidence boundary first.
