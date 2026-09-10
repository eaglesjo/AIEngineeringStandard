# AIEngineeringStandard 2.0 Codex Runtime Adapter

The repository includes a thin Codex adapter at:

```text
scripts/validation/adapters/codex_runtime.py
```

The adapter uses Codex's non-interactive `codex exec` surface. The upstream Codex CLI exposes an explicit `--sandbox/-s` option with `read-only`, `workspace-write`, and `danger-full-access` modes. The conformance adapter deliberately selects `read-only` instead of relying on an implicit default.

References:
- OpenAI Developers: https://developers.openai.com/
- OpenAI Codex source: https://github.com/openai/codex

## Discovery mode

On a machine with Codex installed:

```bash
python scripts/validation/adapters/codex_runtime.py
```

This checks whether the configured executable is available and whether `--version` can be read, then runs the conformance harness in safe dry-run mode. If Codex is absent, the adapter reports `UNTESTED` rather than treating the environment as a failure.

## Runtime mode

The adapter constructs this baseline invocation:

```text
codex exec --ephemeral --sandbox read-only "<scenario prompt>"
```

`--ephemeral` prevents the conformance probe from intentionally persisting session files. `--sandbox read-only` explicitly prevents filesystem writes by the Codex sandbox. The upstream source also exposes separate `workspace-write` and `danger-full-access` modes, which the conformance adapter does not select.

Run an actual probe with:

```bash
export CODEX_BIN=codex
python scripts/validation/adapters/codex_runtime.py \
  --execute \
  --scenario tests/validation/fixtures/conformance/codex-runtime.scenario.json
```

The adapter intentionally does **not** accept an arbitrary `CODEX_RUNTIME_ARGS` environment variable. A free-form argument override could silently widen the sandbox or approval policy and would undermine the purpose of the conformance probe. The runtime command is therefore constructed from a fixed, reviewable safety baseline.

## Network boundary

Read-only filesystem access and network access are separate policy dimensions in Codex. The Codex permission model represents network access explicitly, including for workspace-write mode. Therefore `--sandbox read-only` must not be interpreted by this standard as proof that network access is disabled.

If a scenario requires network denial, the execution environment must enforce and evidence that boundary independently. The conformance result must not promote `permission-check` to `PASS` merely because the model says that it did not use the network.

## Evidence boundary

The adapter records the detected Codex version and passes the invocation to the bounded runtime harness. The harness records repository revision, runtime output, scenario assertions, and protected-file integrity observations.

A successful process exit is **not** sufficient for a `PASS`. In particular, text saying that an operation was refused does not by itself prove that the runtime enforced a permission boundary. Permission enforcement must be supported by observable runtime behavior and protected-state evidence.

## Why this remains an adapter

AIEngineeringStandard is vendor-neutral. The core standard does not depend on Codex-specific CLI syntax. The adapter is responsible for translating the portable conformance scenario into a documented Codex invocation while keeping the safety baseline explicit and reviewable.

The adapter therefore has four responsibilities:

1. Locate the Codex runtime.
2. Record its version.
3. Construct the documented non-interactive entry point with an explicit read-only sandbox.
4. Hand execution to the bounded, evidence-producing conformance harness.

The core standard remains independent of Codex-specific runtime policy.
