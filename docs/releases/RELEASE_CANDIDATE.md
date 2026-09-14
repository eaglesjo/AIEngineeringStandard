# Release Candidate

This document records the public 2.0.0 release-candidate scope. It does not by itself authorize publication.

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
- AI code-quality verification
- AI/LLM evaluation
- provenance and traceability validation
- data/model reproducibility validation
- final CI validation of the exact release-candidate revision

## Release candidate invariants

- Version metadata must consistently identify `2.0.0`.
- Release documentation must describe the current 2.0 scope.
- Historical release tags and commits must remain unchanged.
- The candidate must originate from the canonical development repository and be promoted only after applicable validation passes.
- The final public candidate must receive an independent audit before release authorization.
- Unavailable runtime evidence remains explicitly `UNTESTED` or `SKIPPED`.

## Release version

`2.0.0`

## Publication gate

**NOT AUTHORIZED YET.** Passing release-candidate checks is necessary but not sufficient. The final public audit and explicit release authorization must be completed before the `v2.0.0` tag and GitHub Release are created.
