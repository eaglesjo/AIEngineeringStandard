# Release Candidate

This file marks the `codingStandard-dev` branch as a **2.0.0 release-candidate preparation** surface. It does not authorize publication.

## Required checks

- repository and architecture validation
- policy and dependency-contract validation
- multilingual i18n completeness, semantic parity, and consistency
- installer integration, lifecycle, and fresh-project validation
- Windows PowerShell validation
- deterministic RAG integration and quality gates
- LLM and Vision CPU memory smoke tests
- Google Colab runtime and notebook validation
- executable agent-conformance schema/policy validation
- dependency alignment and isolated real pip resolver integration
- final CI validation of the exact release-candidate commit

## Release candidate invariants

- Version metadata must consistently identify `2.0.0`.
- Release documentation must describe the current 2.0 scope rather than a historical 1.x release.
- Historical 1.x tags and commits must remain unchanged.
- The candidate must originate from `codingStandard-dev` and be promoted only after applicable validation passes.
- The final public candidate must receive a second full audit before release authorization.
- Unavailable runtime evidence remains explicitly `UNTESTED` / `SKIPPED`.

## Release version

`2.0.0`

## Publication gate

**NOT AUTHORIZED YET.** Passing this preparation branch's checks is necessary but not sufficient. Promotion and the independent final public audit are still required before the `v2.0.0` tag/release may be created.
