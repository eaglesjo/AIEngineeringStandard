# Release Status

## Current release

Release: **2.1.0**

Status: **release candidate**

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

## CI and execution

GitHub Actions CI is part of the validation architecture. It runs the repository validation and installer lifecycle gates for pull requests and pushes to `main). Release publication remains governed by the release preflight and publication contract, while CI provides automated evidence that the repository state passes the standard validation gate.

The execution mission contract under `core/runtime/execution/` keeps remote execution bounded, source-identified, least-privileged, and verifiable.

## Release invariants

- Preserve all historical tags and commits.
- Do not reintroduce a separate development or promotion repository.
- Keep `main` releasable.
- Release tags must match `VERSION`.
- Do not describe unavailable runtime evidence as passed.

## v2.1 release readiness

The v2.1 multi-agent architecture and reference runtime have completed the contract, lifecycle, provenance, identity, lineage, evaluation, parallel-work, human-approval, and runtime/schema alignment work required for the 2.1.0 release candidate.

The 2.1.0 release candidate must pass the complete repository validation gate, installer lifecycle validation, v2.1 contract validation, and reference-runtime conformance tests before publication.
