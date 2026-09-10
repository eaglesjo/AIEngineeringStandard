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
7. Per-check evidence for discovery, Skill loading, permissions, execution, validation, recovery, and reporting.
8. Explicit `UNTESTED` for capabilities not exercised by the scenario.

### Promotion rule

- `UNTESTED` means no runtime evidence exists.
- `PASS` requires deterministic runtime evidence for the capability.
- `PARTIAL` records documented limitations.
- `ADAPTER` requires a documented adapter plus runtime evidence through that adapter.
- `UNSUPPORTED` requires evidence that the capability cannot satisfy the contract.
- `FAIL` records a deterministic contract violation.

**No runtime evidence = no PASS.**

## Codex P0 path

The first runtime target is Codex. The initial scenario verifies instruction discovery, portable Skill discovery/loading, controlled task execution, deterministic validation, and evidence reporting. Plugin, MCP, permission-denial, and failure-recovery checks remain `UNTESTED` until dedicated runtime probes are executed.

The repository's static conformance fixture remains separate from runtime evidence so a committed expectation can never be mistaken for real agent execution evidence.
