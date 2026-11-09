# Release Status

## Current release

Release: **2.2.1**

Status: **published**

- GitHub Release: https://github.com/eaglesjo/AIEngineeringStandard/releases/tag/v2.2.1
- PyPI package: https://pypi.org/project/ai-engineering-standard/2.2.1/
- Release tag: `v2.2.1`
- Current repository main is newer than the release tag; changes merged after `v2.2.1` are not part of the published package unless a later release is explicitly created.

## Repository model

`AIEngineeringStandard` is the only source for implementation, validation, and release.

The former `codingStandard-dev` → `AIEngineeringStandard` promotion boundary is retired.

## Validation focus

- canonical repository architecture and policy profile validation
- repository dependency and layer-boundary validation
- environment contract and resource detection validation
- Korean runtime resource completeness, semantic policy parity, and runtime/documentation consistency
- installer lifecycle and obsolete-file reconciliation
- LLM and Vision CPU memory smoke tests
- Google Colab runtime and notebook validation
- deterministic RAG regression and quality-gate coverage
- executable agent-conformance schema/policy validation
- dependency compatibility and resolver validation
- final release-gate validation on the exact tagged commit
- v2.1 canonical multi-agent contract validation
- release preflight checks for remote tag collisions and successful GitHub Actions CI on the exact current `main` commit

## CI and execution

GitHub Actions CI is part of the validation architecture. It runs repository validation, installer lifecycle gates, release-preflight regression tests, Python compatibility checks, platform installer checks, and installable-package validation for pull requests and pushes to `main`. Release publication remains governed by the release preflight and publication contract, while CI provides automated evidence that the repository state passes the standard validation gate.

The execution mission contract under `core/runtime/execution/` keeps remote execution bounded, source-identified, least-privileged, and verifiable.

## Release invariants

- Preserve all historical tags and commits.
- Do not reintroduce a separate development or promotion repository.
- Keep `main` releasable.
- Release tags must match `VERSION`.
- Do not describe unavailable runtime evidence as passed.
- A successful validation or preflight run is not itself authorization to publish a release.
- Never move or overwrite an existing release tag to recover from a partial publication failure.

## v2.1 release record

The v2.1 multi-agent architecture and reference runtime have completed the contract, lifecycle, provenance, identity, lineage, evaluation, parallel-work, human-approval, and runtime/schema alignment work required for the published 2.1.0 release.

The published `v2.1.0` release was created from the validated `main` history. Future releases must continue to pass the complete repository validation gate, installer lifecycle validation, v2.1 contract validation, and applicable reference-runtime conformance tests before publication.
