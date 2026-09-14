# Public Release Process

This document describes how validated AI Engineering Standard releases reach the public distribution repository.

## Repository roles

```text
codingStandard-dev  →  AIEngineeringStandard
implementation and      public distribution
validation
```

- `codingStandard-dev` is the canonical implementation, integration, testing, and release-candidate validation surface.
- `AIEngineeringStandard` is the public distribution surface.

Public releases are not developed directly in the release repository. A release candidate must first pass the applicable validation gates in the development repository and then be promoted as an exact validated revision.

## 2.0.0 release sequence

1. Align version and release metadata in `codingStandard-dev`.
2. Validate the complete repository and release-candidate contract in CI.
3. Record the exact validated development revision and evidence.
4. Promote that exact validated scope to `AIEngineeringStandard`.
5. Perform an independent audit of the final public candidate.
6. Authorize publication only when the required audit and evidence are complete.
7. Create the `v2.0.0` tag and GitHub Release from the audited public commit.

## Evidence rules

- Record exact commit SHAs for source, promotion, and final public identity.
- Treat CI as execution evidence only when the corresponding workflow actually completed successfully.
- Mark unavailable checks explicitly as `UNTESTED`, `UNSUPPORTED`, `SKIPPED`, or `BLOCKED` as appropriate.
- Never convert missing live-runtime evidence into a pass by assumption.
- Preserve historical release tags and commits.

## Release gate

A release is blocked if version metadata is inconsistent, release documentation describes an obsolete target, applicable validation is failing, provenance is incomplete, or the final public candidate has not received the required independent audit.
