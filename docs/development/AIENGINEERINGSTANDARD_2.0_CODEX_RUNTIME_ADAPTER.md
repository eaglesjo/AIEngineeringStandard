# AIEngineeringStandard 2.0 Codex Runtime Adapter

The repository includes a thin Codex adapter at:

```text
scripts/validation/adapters/codex_runtime.py
```

The adapter uses Codex's documented non-interactive `codex exec` surface. OpenAI documents `codex exec` specifically for scripts and CI, with a prompt supplied as a single argument; it runs in a read-only sandbox by default. citeturn2view0

## Discovery mode

On a machine with Codex installed:

```bash
python scripts/validation/adapters/codex_runtime.py
```

This checks whether the configured executable is available and whether `--version` can be read, then runs the conformance harness in safe dry-run mode. If Codex is absent, the adapter reports `UNTESTED` rather than treating the environment as a failure.

## Runtime mode

The adapter constructs this baseline invocation:

```text
codex exec --ephemeral "<scenario prompt>"
```

`--ephemeral` prevents the conformance probe from intentionally persisting session rollout files. OpenAI documents this option for non-interactive runs. citeturn2view0

Run an actual probe with:

```bash
export CODEX_BIN=codex
python scripts/validation/adapters/codex_runtime.py \
  --execute \
  --scenario tests/validation/fixtures/conformance/codex-runtime.scenario.json
```

For runtime-specific, version-validated options, use `CODEX_RUNTIME_ARGS`:

```bash
export CODEX_RUNTIME_ARGS='--ignore-user-config --ignore-rules'
python scripts/validation/adapters/codex_runtime.py --execute
```

The adapter does not invent approval, sandbox, network, or authentication settings. If a workflow needs write access, that permission must be explicitly configured and documented; OpenAI's current guidance recommends explicit sandbox settings for automation and identifies `workspace-write` as the edit-enabled mode. citeturn2view0

## Evidence boundary

The adapter records the detected Codex version and passes the invocation to the bounded runtime harness. The harness records repository revision, runtime output, scenario assertions, and protected-file integrity observations.

A successful process exit is **not** sufficient for a `PASS`. In particular, text saying that an operation was refused does not by itself prove that the runtime enforced a permission boundary. Permission enforcement must be supported by observable runtime behavior and protected-state evidence.

## Why this remains configurable

AIEngineeringStandard is vendor-neutral. Hard-coding one Codex invocation beyond the stable `codex exec` entry point would make the standard brittle across CLI versions and execution environments.

The adapter therefore has four responsibilities:

1. Locate the Codex runtime.
2. Record its version.
3. Construct the documented non-interactive entry point.
4. Hand execution to the bounded, evidence-producing conformance harness.

The core standard remains independent of Codex-specific runtime policy.
