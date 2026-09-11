# AIEngineeringStandard 2.0 Dependency Conflict Resolution Policy

## Purpose

This policy defines the minimum behavior required when an agent encounters incompatible, unsatisfied, or otherwise conflicting software dependencies in a project environment.

It is additive to the 1.x standard and applies to Python packages, system packages, runtime/framework dependencies, and other versioned components that can affect reproducible execution.

## Core principle

Dependency changes are engineering changes, not installation conveniences. An agent must diagnose the environment and dependency graph before changing versions, must prefer the smallest compatible change, and must produce reproducible evidence that the resolved environment still works.

The normative lifecycle is:

```text
Discover → Detect → Measure → Resolve → Smoke Test → Lock → Implement → Validate → Record
```

## Required behavior

### 1. Discover the actual environment

Before resolving a conflict, the agent MUST inspect the relevant execution environment, including when available:

- Python/runtime version;
- operating system and architecture;
- installed package versions;
- declared direct dependencies;
- transitive dependencies and dependency constraints;
- active virtual environment, notebook kernel, container, or other isolation boundary;
- relevant framework, accelerator, and system-library versions.

The agent MUST NOT assume that the dependency declaration is identical to the installed environment.

### 2. Detect and classify the conflict

The agent MUST identify the actual incompatibility before changing dependencies.

At minimum, distinguish:

- direct dependency conflict;
- transitive dependency conflict;
- runtime/framework compatibility conflict;
- Python/OS/architecture compatibility conflict;
- system-library or binary compatibility conflict;
- stale or inconsistent environment state.

The diagnosis SHOULD identify the packages, constraints, and versions that create the conflict.

### 3. Measure before modifying

The agent MUST establish a baseline sufficient to determine whether the environment currently works and what behavior is at risk.

Useful evidence includes dependency-tree output, resolver errors, import failures, package metadata, and a minimal reproducible failing command or test.

An agent MUST NOT treat a generic package-manager error as proof of the root cause without examining the relevant constraints.

### 4. Resolve conservatively

The agent MUST prefer the smallest change that produces a compatible environment.

The agent MUST NOT perform broad or unexplained upgrades/downgrades such as indiscriminate `upgrade all`, `pip install -U` across the environment, or equivalent destructive operations merely to suppress a resolver error.

Resolution choices SHOULD follow this order when practical:

1. remove an unnecessary dependency;
2. align a direct dependency with an already-supported constraint;
3. select a compatible version within the declared range;
4. update a tightly related dependency set when required;
5. revise the dependency declaration/lock only when the resulting combination is validated.

If no compatible solution exists under the current project constraints, the agent MUST report the conflict rather than silently weakening or bypassing the constraints.

### 5. Isolate risky changes

Dependency modifications SHOULD be performed in an isolated environment when practical, such as a virtual environment, temporary environment, container, or disposable CI job.

An agent MUST preserve the user's existing environment when an isolated validation path is reasonably available.

If the active environment must be modified, the agent SHOULD capture the pre-change dependency state so that recovery is possible.

### 6. Smoke test immediately

After a candidate resolution, the agent MUST perform a minimal smoke test that covers the affected dependency boundary.

A suitable smoke test may include:

- successful installation/resolution;
- successful import of affected packages;
- version/API compatibility check;
- minimal execution of the affected feature;
- targeted test reproducing the original failure.

A successful package installation alone is NOT sufficient evidence that a dependency conflict has been resolved.

### 7. Validate for regression

A resolved environment MUST be checked for regressions in previously working functionality that depends on the changed packages.

Validation SHOULD proceed from the smallest meaningful affected test to the broader project test suite.

If validation fails because another dependency became incompatible, the candidate resolution MUST be rejected or further resolved rather than declared successful.

### 8. Lock the resolved state

When a dependency conflict is resolved, the resulting compatible versions MUST be made reproducible through the project's supported dependency mechanism, such as a lockfile, pinned requirements, or equivalent version constraints.

The record SHOULD distinguish:

- directly selected versions;
- transitively resolved versions;
- environment/runtime constraints;
- platform-specific constraints, when applicable.

Locking MUST NOT be represented as proof of runtime correctness by itself; execution validation is still required.

### 9. Recover on failed resolution

If a dependency change breaks the environment or fails validation, the agent MUST either:

- restore the pre-change dependency state; or
- continue from a controlled isolated environment without contaminating the known-good environment.

The agent MUST record the failed candidate when that information is useful for preventing repeated failures.

### 10. Record evidence

A dependency-resolution result SHOULD record enough information to reproduce and audit the decision, including:

- standard version;
- repository revision;
- runtime/environment identity;
- dependency state before resolution;
- conflict diagnosis;
- candidate changes considered or applied;
- final resolved versions/constraints;
- smoke-test result;
- regression-test result;
- timestamps;
- provenance of package metadata and test output.

Evidence MUST distinguish a package-manager resolution result from actual runtime validation.

## Security and integrity boundaries

Dependency installation and resolution are executable operations and MUST be treated as untrusted changes to the environment.

An agent MUST NOT:

- expose credentials or private package indexes in logs or evidence;
- execute arbitrary installation commands unrelated to the diagnosed conflict;
- bypass package or repository security policies merely to obtain a successful resolver result;
- claim a dependency is safe solely because it can be installed.

Secrets, credentials, and authenticated package-index configuration MUST remain outside source-controlled dependency evidence.

## Conformance mapping

Dependency conflict resolution primarily contributes evidence to these 2.0 checks:

| Conformance check | Dependency-resolution evidence |
| --- | --- |
| `task-execution` | The affected task executes with the resolved environment |
| `validation` | Smoke and regression tests pass |
| `failure-recovery` | Failed candidate changes are safely reverted or isolated |
| `evidence-reporting` | Conflict, resolution, versions, and validation are recorded |
| `permission-check` | Only when dependency operations exercise a defined permission boundary |

Dependency resolution MUST NOT be inferred from static presence of a requirements file, lockfile, or installed package.

## Minimum acceptance criteria

A dependency conflict is considered **resolved** only when all applicable conditions are satisfied:

1. The actual environment and dependency constraints were inspected.
2. The conflict was diagnosed or bounded to a reproducible failure.
3. A compatible candidate was selected without an unjustified broad dependency change.
4. The affected packages install/resolve successfully.
5. The affected runtime boundary passes a smoke test.
6. Relevant regression validation passes.
7. The final environment is reproducible through the project's dependency mechanism.
8. The result and evidence are recorded.

If any required condition is not satisfied, the agent MUST report the state as unresolved, partial, or untested rather than claiming successful resolution.

## Non-goals

This policy does not mandate one package manager, lockfile format, resolver, operating system, or dependency-management tool. Projects may use the mechanism appropriate to their runtime, provided that the resulting environment remains diagnosable, reproducible, and validated.
