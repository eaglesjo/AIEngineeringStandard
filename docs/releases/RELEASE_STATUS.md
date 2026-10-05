# Release Status

## Current release

Release: **2.0.2**

Status: **published**

## Repository model

`AIEngineeringStandard` is the only source for implementation, validation, and release.

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
- v2.1 canonical multi-agent contract validation

## Release invariants

- Preserve all historical tags and commits.
- Do not reintroduce a separate development or promotion repository.
- Keep `main` releasable.
- Release tags must match `VERSION`.
- Do not describe unavailable runtime evidence as passed.

## v2.1 development boundary

v2.1 architecture and contract work is developed in temporary branches and merged to `main` only after the v2.0 validation gates and the v2.1 contract gate pass.

The next release version is assigned only when v2.1 implementation work is release-ready.
