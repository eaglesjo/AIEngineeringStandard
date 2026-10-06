# Repository Execution Contract

## Purpose

The repository execution layer defines how AI Engineering Standard performs repository work across a disposable sandbox and GitHub Actions without making either environment the canonical source of truth.

The canonical repository state is a Git commit identified by an immutable SHA. Execution is bounded by an explicit mission contract and completion is supported by Evidence.

## Execution model

Intent -> exact repository state -> sandbox-first execution -> bounded GitHub Actions execution when needed -> output verification -> Evidence -> Evaluation/Acceptance -> durable Git state.

GitHub Actions is an execution mechanism, not a second source of truth and not an interactive remote shell.

## Mission contract

Every bounded Actions execution should have:

- source repository and immutable source SHA;
- explicit purpose;
- explicit inputs;
- explicit operations;
- expected outputs;
- minimum permissions;
- terminal state;
- verification requirements.

The machine-readable contract is `mission.schema.json`.

## Operating rules

1. Resolve mutable branch or PR names to a commit SHA before consequential execution.
2. Prefer the sandbox work environment for editing, debugging, and iterative development.
3. Use Actions for bounded CI, build, test, transport, supply, or recovery work when that is safer or more reliable than the available local path.
4. Never treat a successful workflow status as sufficient evidence by itself.
5. Verify the source SHA and relevant outputs after execution.
6. Diagnose a failed run before retrying it.
7. Temporary workflows, artifacts, and branches are task-owned state and must be cleaned up after terminal use.
8. Do not put secrets into workflow text, artifacts, logs, or mission payloads.
9. Do not grant write permissions to jobs that only validate source.
10. Remote execution must remain distinguishable from local execution in evidence and reporting.

## Relationship to v2.1

Execution missions are runtime adapters around the canonical v2.1 model. They do not redefine Agent, Work Unit, Evidence, Evaluation, or Acceptance semantics.

A mission may be attached to a Work Unit as execution evidence. The Work Unit remains the canonical trace boundary.
