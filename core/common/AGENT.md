# Common AI Agent Rules

These rules apply to every supported project domain.

1. Inspect the actual repository, runtime, dependencies, tests, and security constraints before changing code.
2. Detect and measure the real execution environment before choosing resource-sensitive settings.
3. Do not hard-code a specific machine, OS, CPU, RAM, GPU, accelerator, or IDE as a project prerequisite.
4. Keep reusable domain logic in modules and keep notebooks/scripts focused on orchestration.
5. Use explicit configuration, reproducibility metadata, and deterministic paths.
6. Preserve secrets outside source control.
7. Validate changes with the smallest meaningful test first, then run the broader test suite.
8. After environment validation, remove unused execution branches and obsolete code unless multi-platform support is intentional.
9. Long-running workloads should use validation, Early Stopping where meaningful, best Checkpoint, and Resume.
10. Experiments should define a baseline, controlled variants, seeds, metrics, and resource tracking.
11. Before adding or changing a developer-selected dependency, inspect authoritative compatibility constraints and the actual dependency graph; preserve the selected version as the compatibility anchor, align only affected dependencies, and validate before locking.
12. When dependency conflicts occur, inspect the actual dependency graph and runtime before changing versions; resolve conservatively, smoke-test the affected boundary, validate regressions, lock the resolved state, and preserve a recovery path. Follow `core/validation/dependency-conflict-resolution-policy.md`.
13. Do not use broad or unexplained dependency upgrades/downgrades merely to suppress resolver errors.

## Standard execution lifecycle

```text
Discover → Detect → Measure → Resolve → Smoke Test → Lock → Implement → Validate → Record
```
