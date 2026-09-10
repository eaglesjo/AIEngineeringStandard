# AIEngineeringStandard 2.0 Runtime Conformance

## Purpose

The runtime conformance harness converts the 2.0 conformance protocol into a reproducible evidence workflow. Static inspection establishes repository contracts; runtime execution is required before an agent can be promoted from `UNTESTED` to an evidence-backed support status.

## Components

- `core/validation/conformance-evidence.schema.json` — machine-readable runtime evidence contract.
- `tests/validation/fixtures/conformance/codex-runtime.scenario.json` — deterministic Codex P0 scenario.
- `scripts/validation/run_runtime_conformance.py` — bounded runtime harness.

## Safety boundary

The harness does **not** execute Skill, Plugin, or MCP code directly. It invokes only the explicitly supplied agent runtime command. The scenario prompt, timeout, output capture, and deterministic assertions are controlled by the harness.

Runtime tests must be run in an environment where the agent's filesystem, network, secrets, and destructive-operation permissions are explicitly bounded by the runtime/platform. A successful process exit is not sufficient evidence of permission enforcement.

## Evidence model

Runtime evidence separates **what the harness can observe** from **what the agent says it did**. Every observation records:

- `source`: `harness`, `adapter`, or `runtime`.
- `method`: one of `task-assertion`, `harness-integrity`, `adapter-trace`, or `direct-runtime`.
- `evidence_level`: `weak`, `moderate`, or `strong`.
- `result`: `OBSERVED`, `NOT_OBSERVED`, or `FAILED`.

Evidence levels are normative guidance:

| Level | Meaning | Example |
| --- | --- | --- |
| `weak` | Assertion derived from task output; useful for deterministic task checks but not proof of internal runtime behavior. | Model output contains `portable-skill`. |
| `moderate` | Objective harness/adapter observation of process or invocation behavior. | Runtime exited with code 0; adapter recorded an exact invocation. |
| `strong` | Objective integrity or runtime/adapter trace that directly establishes the capability event. | Protected-file hash is unchanged, or a runtime event explicitly records Skill loading. |

A `strong` harness-integrity observation of an unchanged file proves the file was not changed during the probe; it does **not** by itself prove that the runtime enforced a denied permission. Permission PASS therefore requires an appropriate runtime/adapter enforcement observation when the claim is specifically about enforcement.

Likewise, task-output markers never prove instruction discovery or Skill loading. Those checks remain `UNTESTED` until an adapter or runtime supplies an objective discovery/loading observation.

## Dry run

The default mode emits a complete evidence-shaped result with every check set to `UNTESTED`:

```bash
python scripts/validation/run_runtime_conformance.py \
  --agent codex \
  --output /tmp/codex-runtime-conformance.json
```

This mode is safe for normal CI and does not invoke an agent runtime.

## Runtime execution

Runtime execution is explicit. Use `{prompt}` in `--command` where the scenario prompt should be inserted:

```bash
python scripts/validation/run_runtime_conformance.py \
  --agent codex \
  --runtime-version '<runtime-version>' \
  --command 'YOUR-CODEX-RUNTIME {prompt}' \
  --execute \
  --output /tmp/codex-runtime-conformance.json
```

The exact command is intentionally supplied by the test environment rather than hard-coded into the standard. This keeps the standard vendor-neutral and permits hosted, CLI, IDE, or managed-agent runners.

## Evidence requirements

A runtime result should include:

1. Agent identifier and runtime version.
2. Immutable repository revision and dirty-state observation.
3. Scenario identifier and deterministic task description.
4. Start/end timestamps.
5. Process exit status and timeout observation.
6. Bounded stdout/stderr excerpts.
7. Protected-file integrity observations when a negative probe uses protected files.
8. Per-check evidence for discovery, Skill loading, permissions, execution, validation, recovery, and reporting.
9. Explicit `UNTESTED` for capabilities not exercised by the scenario.
10. Objective observations for any capability promoted to `PASS`.

### Promotion rule

- `UNTESTED` means no sufficient runtime evidence exists.
- `PASS` requires deterministic runtime evidence appropriate to the capability being claimed.
- `PARTIAL` records documented limitations or incomplete capability coverage.
- `ADAPTER` requires a documented adapter plus runtime evidence through that adapter.
- `UNSUPPORTED` requires evidence that the capability cannot satisfy the contract.
- `FAIL` records a deterministic contract violation.

**No sufficient runtime evidence = no PASS.**

## Codex P0 path

The first runtime target is Codex. The initial scenario verifies deterministic task behavior and repository integrity while intentionally leaving instruction discovery, Skill discovery/loading, Plugin, MCP, and runtime permission-enforcement claims unpromoted until objective runtime/adapter observations are available.

The repository's static conformance fixture remains separate from runtime evidence so a committed expectation can never be mistaken for real agent execution evidence.

## Future adapter contract

A runtime adapter that can expose native events or traces should map those events into observations using `method: "adapter-trace"` or `method: "direct-runtime"` and `evidence_level: "strong"` where the event directly establishes the claimed capability. The adapter must preserve the original event meaning and must not manufacture observations from model text.

If a runtime exposes no trustworthy discovery/loading telemetry, the correct result is `NOT_OBSERVED` and the related conformance check remains `UNTESTED`. The standard prefers an honest `UNTESTED` result over an inferred `PASS`.
