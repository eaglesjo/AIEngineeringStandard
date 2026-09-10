# AIEngineeringStandard 2.0 Conformance Policy

## Purpose

This document defines the normative interpretation of 2.0 conformance results and the minimum evidence required to promote an agent from an untested compatibility declaration to an observed conformance state.

The policy is additive to the 1.x standard. It does not change existing 1.x behavior.

## Result states

The result state is a claim about the tested agent/runtime combination, not a permanent property of the agent.

| Result | Meaning | Minimum condition |
| --- | --- | --- |
| `UNTESTED` | No sufficient execution evidence exists | Checks are only `UNTESTED` or `UNSUPPORTED` |
| `UNSUPPORTED` | A required capability is not available in the tested environment | The unsupported capability is explicitly identified |
| `ADAPTER` | Conformance is observed through an adapter boundary, without sufficient direct runtime evidence for full conformance | At least one relevant check is `ADAPTER` or `PASS` |
| `PARTIAL` | Some required behavior is observed, but full conformance is not established | All mandatory checks are present; no check is `FAIL`; at least one check is non-`PASS` |
| `PASS` | All mandatory conformance checks passed | All mandatory checks are present and every check is `PASS` |
| `FAIL` | A required behavior failed | At least one required check is `FAIL` |

`PASS` must never be inferred from the absence of failures. Positive evidence is required for every mandatory check.

## Evidence levels

Evidence observations use three levels:

- `weak`: static inspection, metadata, or indirect harness evidence.
- `moderate`: adapter traces, deterministic harness assertions, or integrity checks tied to a specific scenario.
- `strong`: direct runtime observation with reproducible invocation and attributable output.

Evidence level describes strength of an observation; it does not override a failed check.

## Promotion policy

Compatibility status should progress conservatively:

`UNTESTED -> ADAPTER -> PARTIAL -> PASS`

A result may remain `UNTESTED` when the runtime cannot be exercised. `UNSUPPORTED` is a capability/environment state and is not itself evidence of conformance.

Promotion requires:

1. a pinned standard version;
2. a specific agent identity and runtime version when available;
3. a repository revision or equivalent immutable test target;
4. a named scenario;
5. start and finish timestamps;
6. check-level results;
7. observations that explain the evidence for each promoted check;
8. enough provenance to distinguish harness, adapter, and direct runtime evidence.

A single weak observation must not promote an agent to `PASS`.

## Security and permissions

Protected-file integrity proves that a protected file was unchanged between observations. It does **not** prove that the runtime would have denied a write.

A permission check may be promoted to a strong security claim only when the scenario records an attempted protected operation and the runtime demonstrably denies it, while the protected target remains unchanged.

Likewise, a post-run hash check is valid supporting evidence but must not be labeled as runtime-enforced denial by itself.

## Provenance requirements

Evidence is attributable only when its source and method are explicit. The supported observation sources are:

- `harness` — deterministic test harness evidence;
- `adapter` — evidence emitted or interpreted by a runtime adapter;
- `runtime` — direct runtime evidence.

The supported observation methods are:

- `task-assertion`;
- `harness-integrity`;
- `adapter-trace`;
- `direct-runtime`.

Evidence artifacts should be retained with the tested revision and scenario so that a later reviewer can distinguish a repeatable test from an informal declaration.

## Compatibility catalog rule

`compatibility/agents.json` is a target/status catalog, not proof by itself. New agents and capabilities must default to `UNTESTED` until evidence satisfies this policy.

A release may advertise an agent as conformant only when the corresponding evidence is available and the declared status agrees with the evidence-backed result.

## Non-goals

This policy does not require every supported agent to expose identical internal events. Adapters may normalize vendor-specific telemetry into the standard evidence model. Missing first-class events must remain `NOT_OBSERVED` rather than being inferred from incidental file access or metadata.
