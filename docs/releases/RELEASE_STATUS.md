# Release Status

## Current target

Release target: **2.0.2**

Status: **local-first CI/release architecture**

## Repository model

`AIEngineeringStandard` is now the only source for implementation, validation, and release.

The former `codingStandard-dev` → `AIEngineeringStandard` promotion boundary is retired.

## Validation focus

- canonical repository architecture and policy profile validation
- repository dependency and layer-boundary validation
- environment contract and resource detection validation
- multilingual runtime resource completeness, semantic policy parity, and runtime/documentation consistency
- installer lifecycle and obsolete-file reconciliation
- LLM and Vision CPU memory smoke tests
- Google Colab runtime and notebook validation
- deterministic RAG regression and quality-gate coverage
- executable agent-conformance schema/policy validation
- dependency compatibility and resolver validation
- final release-gate validation on the exact tagged commit

## Release invariants

- Preserve all historical tags and commits.
- Do not reintroduce a separate development or promotion repository.
- Keep `main` releasable.
- Release tags must match `VERSION`.
- Do not describe unavailable runtime evidence as passed.

## Gate

`v2.0.2`: **release candidate**

Required sequence:

`development → local validation → main → release preflight → annotated tag → GitHub Release`.
