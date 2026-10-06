# Repository Execution Policy

## Purpose

This policy defines the standard way an AI engineering agent uses disposable execution environments and GitHub Actions while keeping Git history as the durable source of truth.

The policy is intentionally host-neutral. It describes capabilities and safety boundaries; an integration must use only the repository, sandbox, GitHub, Actions, log, artifact, and credential operations that it actually has.

## Execution priority

1. Resolve the target repository and mutable ref to an immutable commit SHA.
2. Materialize and verify that exact source before editing or iterative execution.
3. Prefer the sandbox work environment for editing, building, testing, debugging, and inspection.
4. Use GitHub Actions only for bounded validation, supply, transport, recovery, cleanup, or remote execution that the sandbox cannot safely or efficiently provide.
5. Verify returned outputs and source identity before consuming them.
6. Persist meaningful results as Git commits, pull requests, or immutable artifacts.
7. Clean task-owned temporary remote state only after terminal status and ownership are established.

Actions is an execution mechanism, not an interactive remote shell and not a second source of truth.

## Bounded execution mission

Every remote execution must be representable as a bounded mission with:

- repository identity;
- immutable source SHA;
- purpose;
- exact inputs;
- explicit operations;
- expected outputs;
- integrity/provenance requirements;
- minimum permissions;
- trust boundary;
- terminal state;
- verification requirements.

The machine-readable contract is `core/runtime/execution/mission.schema.json`.

If the expected source SHA no longer matches, stop the mission path and recover the current durable state before continuing.

## Mission classes

### Supply

Use a supply mission when the sandbox can perform the engineering work but cannot obtain a required external input.

The mission must identify the target platform, acquire only the required input, record provenance, checksum the result, and verify compatibility before sandbox consumption.

### Transport

Use a transport mission when exact source or an exact verified result must cross an environment boundary.

Prefer direct text/file operations for small semantic changes. Prefer Git objects, bundles, archives, or artifacts for opaque, binary, or filesystem-sensitive state. Verify checksums and expected Git tree/source identity at both ends.

### Degraded remote execution

Use degraded remote execution only when the sandbox itself is unavailable or cannot faithfully sustain the requested engineering loop.

Remote work remains bounded: establish the durable base, perform one bounded step, persist the result, inspect evidence, then decide the next step. Do not treat a runner as a persistent workstation.

## Failure diagnosis and retry

A failed workflow is evidence to inspect, not a reason to guess.

Before retrying:

1. inspect the workflow conclusion and failed job/step;
2. inspect the relevant logs;
3. inspect produced artifacts, commits, refs, or partial results;
4. classify the failure when possible as source/test failure, mission defect, permission/authentication failure, quota/platform limit, stale source identity, or transient infrastructure failure;
5. change the mission or execution path when evidence requires it.

Do not repeatedly rerun an unchanged failed mission without evidence of a transient failure. A green workflow is not sufficient completion evidence; verify the outputs required by the mission.

## Task ownership and cleanup

Temporary branches, workflow definitions, artifacts, transport payloads, and mission-only files must be task-owned.

Use collision-resistant mission identifiers. Keep unrelated work out of shared temporary state.

Do not delete unfamiliar remote state. Before destructive cleanup, re-resolve mutable refs and confirm ownership and terminal status. Cleanup must be idempotent.

Keep failed runs and artifacts while they have diagnostic or recovery value. Remove or shorten retention of obsolete task-owned state after a newer durable result supersedes it.

## Security boundary

AI-authored workflow and mission state must not contain secret values.

Use the smallest available workflow permissions. Validation-only jobs should normally use read-only repository access.

Do not execute untrusted issue, pull-request, ref, label, or artifact content with secrets or write-capable credentials.

Downloaded executables and artifacts require provenance verification before execution or consumption.

## Recovery

When chat context, sandbox state, or an execution attempt is lost, recover in this order:

```text
commit / PR head
    > immutable Git or Actions artifact
    > surviving sandbox working tree
    > conversation reconstruction
```

Compare recovered state with surviving work before replacing or merging it. Preserve unfamiliar changes until ownership is understood.

## Evidence boundary

Execution results are evidence attached to the relevant Work Unit. They do not redefine Agent, Work Unit, Handoff, Evidence, Evaluation, or Acceptance semantics.

Completion claims must identify the exact source state and the checks that actually ran.
