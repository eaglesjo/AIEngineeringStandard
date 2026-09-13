# Release Process

This document defines the release boundary for AI Engineering Standard.

## Repository roles

```text
codingStandard-private  →  codingStandard-dev  →  AIEngineeringStandard
        Luna/internal          implementation/validation       public release
```

- `codingStandard-private` contains Luna activation, continuity state, history, and internal operating policy.
- `codingStandard-dev` is the implementation, integration, testing, and release-candidate validation surface.
- `AIEngineeringStandard` is the public release surface.

A public release must not be developed directly in the release repository before development validation.

## 2.0.0 release sequence

1. Align version and release metadata in `codingStandard-dev`.
2. Validate the complete repository and release-candidate contract in CI.
3. Record the exact validated development SHA and evidence.
4. Promote that exact validated scope to `eaglesjo/AIEngineeringStandard`.
5. Run an independent second full audit on the final public candidate.
6. Authorize release only if the second audit passes and no required evidence is missing.
7. Create the `v2.0.0` tag and GitHub Release from the audited public commit.

## Evidence rules

- Record exact commit SHAs for source, promotion, and final public identity.
- Treat CI as execution evidence only when the corresponding workflow actually completed successfully.
- Mark unavailable checks as `UNTESTED`, `UNSUPPORTED`, `SKIPPED`, or `BLOCKED` as appropriate.
- Never convert missing live-runtime evidence into a pass by assumption.
- Preserve historical release tags and commits.

## Release gate

The release is blocked if version metadata is inconsistent, release documentation describes an obsolete target, applicable validation is failing, provenance is incomplete, or the final public candidate has not received the required second full audit.
