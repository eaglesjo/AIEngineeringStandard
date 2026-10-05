# ML Runtime Validation

This document defines the repository-level contract for validating ML runtime assumptions.

## Scope

Validation covers:

- Python runtime compatibility;
- CPU/GPU/accelerator detection;
- memory and disk availability;
- PyTorch/torchvision compatibility;
- batch-size and sequence-length recommendations;
- smoke-test behavior on constrained environments;
- reproducibility and checkpoint recovery assumptions.

## Policy

Runtime-dependent evidence must be measured on the actual execution environment. A machine profile must not be treated as universal evidence.

When an accelerator or runtime is unavailable, record the result as `UNTESTED`, `UNSUPPORTED`, `SKIPPED`, or `BLOCKED` as appropriate.

## Repository gates

The shared environment profiler is implemented in `core/common/environment.py`. Focused runtime and dependency checks live under `scripts/development/` and `tests/integration/`.

The full release validation entrypoint is:

```bash
python3 scripts/validation/validate.py
```
