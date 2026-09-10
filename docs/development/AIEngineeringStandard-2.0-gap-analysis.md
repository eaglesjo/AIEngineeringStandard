# AIEngineeringStandard 2.0 Implementation Gap Analysis

**Audit baseline:** `main` at `bf4a1cb715215d212db0cfc4ab7cd8571a780a4f`  
**Audit date:** 2026-09-10  
**Scope:** 2.0 machine-readable contracts, agent compatibility, portable Skills, runtime conformance, Codex adapter, fixtures, and CI.

## Executive summary

AIEngineeringStandard 2.0 is **partially implemented as an additive conformance layer**, not yet a complete 2.0 release. The repository already contains the core contract vocabulary, JSON schemas, portable Skill fixture, Codex runtime adapter, bounded runtime harness, and a dedicated 2.0 CI workflow. Existing 1.x behavior remains authoritative during the migration phase.

The largest gap is **evidence depth versus declared compatibility**: the compatibility catalog currently declares every agent and capability as `UNTESTED`, while the CI path only exercises the Codex adapter. The runtime harness can produce real observations when explicitly executed, but the default CI path uses dry-run mode, which intentionally produces `UNTESTED` results. Permission conformance is currently an integrity probe, not proof that the runtime denied an operation.

Therefore the correct 2.0 strategy is to harden the contract and evidence model before broadening vendor adapters. Do not promote the current state as full multi-agent 2.0 conformance.

## Current implementation

| Area | Status | Evidence | Assessment |
|---|---|---|---|
| 2.0 agent compatibility catalog | Implemented | `compatibility/agents.json` | Schema/versioned catalog exists, but all entries are `UNTESTED`. |
| Agent normative layer | Implemented (M1) | `core/agent/README.md` | Defines vendor-neutral execution contract surface; explicitly additive. |
| Conformance result schema | Implemented | `core/validation/conformance-result.schema.json` | Machine-readable result contract exists. |
| Runtime evidence schema | Implemented | `core/validation/conformance-evidence.schema.json` | Captures observations, checks, repository revision, and protected-file hashes. |
| Schema validator | Implemented | `scripts/validation/validate_2_0_schemas.py` | Validates the foundation fixtures and Codex scenarios. |
| Portable Skill contract | Implemented (minimal) | `scripts/validation/validate_portable_skill.py`, fixture | Validates frontmatter/name/body and blocks several secret-like tokens. |
| Runtime conformance harness | Implemented | `scripts/validation/run_runtime_conformance.py` | Bounded execution, marker assertions, JSONL observations, integrity checks. |
| Codex adapter | Implemented (single adapter) | `scripts/validation/adapters/codex_runtime.py` | Discovers `codex`, records version, uses JSONL/read-only baseline, invokes harness. |
| Codex JSONL parser tests | Implemented | CI workflow | Parser and adapter self-tests are part of the 2.0 gate. |
| 2.0 CI gate | Implemented | `.github/workflows/ai-engineering-standard-2.0-conformance.yml` | Runs schema/Skill/parser/adapter/static/runtime/recovery checks. |
| Multi-agent runtime conformance | Missing | Catalog lists many agents, but no equivalent runtime adapters are wired into CI | Needs staged adapter rollout. |
| First-class instruction/Skill discovery evidence | Partial | Harness explicitly records these as `NOT_OBSERVED` for Codex | Contract exists, but Codex JSONL does not expose these as first-class events through the current adapter. |
| Plugin/MCP runtime evidence | Partial | Check IDs and parser support exist; default scenario does not exercise them | Needs dedicated positive/negative scenarios and adapters where possible. |
| Runtime permission denial proof | Partial | Protected-file hashes are checked | Integrity after the run does not prove the runtime itself enforced denial. |
| Trusted evidence/provenance policy | Partial | Evidence includes revision and hashes; security schema exists | Needs an explicit policy tying evidence trust to execution provenance. |

## Key findings

### 1. Compatibility declarations are ahead of evidence

`compatibility/agents.json` is correctly versioned as schema `2.0.0` / standard `2.0`, but all listed agents are `UNTESTED`. This is preferable to fabricating support, but it means the catalog is currently a **compatibility target matrix**, not a verified support matrix.

**Action:** keep `UNTESTED` as the honest default and introduce explicit promotion rules such as `UNTESTED -> ADAPTER -> PARTIAL -> PASS`, with evidence required for every transition.

### 2. CI currently validates the 2.0 machinery, not broad runtime conformance

The 2.0 workflow runs schema validation, portable Skill validation, Codex parser/adapter checks, static conformance, and runtime/recovery harness dry runs. The dry-run path deliberately emits `UNTESTED` evidence instead of executing a live agent.

**Action:** separate CI into two explicit gates:

- **Contract gate:** deterministic, always-on, no external agent required.
- **Runtime evidence gate:** opt-in/controlled execution against an installed adapter, with evidence artifacts and explicit environment/provenance metadata.

This avoids treating a green CI job as proof of live agent conformance.

### 3. Permission conformance is not yet a true enforcement test

The harness protects selected files with SHA-256 hashes and verifies they remain unchanged. The implementation itself notes that this is not proof of runtime-enforced denial.

**Action:** define permission scenarios with an observable denial condition (for example, a command that must fail with a permission/sandbox signal) and separately retain file-integrity checks as a safety backstop.

### 4. Codex event coverage is intentionally conservative

The Codex parser recognizes known lifecycle events and selected item types, but instruction discovery, Skill discovery, and Skill loading are marked `NOT_OBSERVED` when there is no first-class event. Accessing `SKILL.md` is deliberately not promoted to a first-class Skill-loading claim.

**Action:** retain this conservative behavior. Add a normalized adapter observation contract so adapters can report equivalent vendor-specific evidence without weakening the vendor-neutral standard.

### 5. Portable Skill validation is intentionally minimal

The current Skill validator checks YAML-like frontmatter fields, naming, description length, body presence, and several secret-like tokens. It does not execute the Skill, which is the correct security baseline.

**Action:** evolve this into a machine-readable Skill schema and deterministic negative fixtures rather than adding arbitrary parser complexity to the current script.

## 2.0 milestone plan

### M1 — Contract hardening

- Freeze schema identifiers and status semantics.
- Require the complete check vocabulary where a result claims full conformance.
- Define evidence promotion rules.
- Define provenance/trust requirements.
- Add negative fixtures for malformed evidence, forbidden permission behavior, and unsafe Skill metadata.

### M2 — Codex evidence depth

- Add explicit permission-denial scenarios.
- Add MCP capability scenarios where the runtime can expose them safely.
- Improve normalized observation mapping without guessing vendor events.
- Add controlled live-runtime CI as a separate, non-default gate.

### M3 — Adapter framework

- Define a common adapter interface for discovery, version, invocation, event parsing, and capability mapping.
- Keep adapters thin and vendor-specific.
- Add P0 agents incrementally; do not mark unsupported agents as PASS without direct evidence.

### M4 — Release readiness

A 2.0 release candidate should require:

1. Contract gate PASS.
2. All mandatory schemas and fixtures validated.
3. At least one real runtime adapter with reproducible evidence.
4. Permission enforcement tested independently from file-integrity checks.
5. Evidence provenance/trust policy enforced.
6. Compatibility matrix accurately reflecting `PASS`, `PARTIAL`, `ADAPTER`, `UNTESTED`, and `UNSUPPORTED` states.
7. 1.x migration/compatibility documentation complete.

## Immediate next implementation tasks

1. Add a normative 2.0 conformance policy document defining status transitions and evidence requirements.
2. Add negative evidence/security fixtures and validate them in CI.
3. Tighten the result validator so a full conformance result cannot silently omit mandatory checks.
4. Add a dedicated permission-denial scenario and distinguish **enforced denial** from **post-run integrity**.
5. Add adapter-contract tests that every future agent adapter must satisfy.
6. Only then begin P0 adapter expansion.

## Important compatibility rule

2.0 remains additive until a documented migration milestone replaces 1.x authority. This preserves the repository's current migration posture while allowing 2.0 contracts and evidence to mature independently.
