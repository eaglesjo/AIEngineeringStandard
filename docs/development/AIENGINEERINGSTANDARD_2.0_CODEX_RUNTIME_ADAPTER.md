# AIEngineeringStandard 2.0 Codex Runtime Adapter

The repository now includes a thin Codex adapter at:

```text
scripts/validation/adapters/codex_runtime.py
```

The adapter deliberately keeps **runtime policy outside the standard**. It does not guess authentication, sandboxing, network policy, filesystem permissions, or destructive-operation policy. Those controls belong to the environment that launches the Codex runtime.

## Discovery mode

On a machine with Codex installed:

```bash
python scripts/validation/adapters/codex_runtime.py
```

This checks that the configured executable can be located and that `--version` works, then runs the conformance harness in safe dry-run mode.

## Runtime mode

Set the runtime executable and execution arguments explicitly:

```bash
export CODEX_BIN=codex
export CODEX_RUNTIME_ARGS='<runtime-specific arguments>'

python scripts/validation/adapters/codex_runtime.py \
  --execute \
  --scenario tests/validation/fixtures/conformance/codex-runtime.scenario.json
```

The adapter passes the scenario prompt to the configured command and records the exact invocation in the evidence result. A runtime-specific argument set should only be considered valid after confirming the installed Codex version's CLI contract.

## Why this is intentionally configurable

AIEngineeringStandard is a vendor-neutral standard. Hard-coding one Codex CLI invocation would make the standard brittle across CLI versions, hosted runners, managed agents, and future execution surfaces.

The adapter therefore has three responsibilities only:

1. Locate the Codex runtime.
2. Record its version.
3. Hand the invocation to the bounded, evidence-producing conformance harness.

Permission and isolation remain external requirements. A runtime result cannot be promoted to `PASS` merely because the process exited successfully; the evidence must demonstrate the required capability and permission behavior.
