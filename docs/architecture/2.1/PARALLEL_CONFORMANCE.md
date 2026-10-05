# v2.1 Parallel Work Conformance

The parallel conformance fixture demonstrates that parallel work is represented by distinct Work Units rather than implicit scheduler state.

## Scenario

A planner owns a root Work Unit and creates two sibling child Work Units:

- wu-parallel-a owned by implementer-a;
- wu-parallel-b owned by implementer-b.

The two child Work Units have independent identities, owners, contracts, evidence, and evaluations. They share the root only through explicit parent_id lineage.

The root is accepted only after both child evaluations are PASS/ACCEPTED and the planner records explicit join evidence. The fixture therefore demonstrates the required evaluation/acceptance boundary for joining parallel work.

This is a deterministic contract fixture, not a production scheduler. It does not prescribe threads, processes, queues, or a particular orchestration framework.
