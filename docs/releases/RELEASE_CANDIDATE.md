# Release Candidate

This document defines the release-candidate gate for the current single-repository model.

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
- dependency alignment and isolated real pip resolver validation
- final CI validation of the exact release commit

## Release candidate invariants

- `VERSION` is the canonical release version.
- `core/common/environment.py::STANDARD_VERSION` must match `VERSION`.
- Release documentation must describe the current single-repository model.
- Historical tags and commits remain unchanged.
- The candidate is developed and validated in this repository.
- No promotion from another repository is permitted.
- Unavailable runtime evidence remains explicitly `UNTESTED` / `SKIPPED`.

## Current transition

The former `v2.0.0` release remains historical. The next release is `v2.0.1` under the independent development and release contract.

## Publication gate

A `v2.0.1` release is authorized only when the pull request is merged to `main`, the release version is consistent, and the tagged commit passes the release workflow.
