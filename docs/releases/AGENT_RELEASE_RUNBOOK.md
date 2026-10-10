# Agent Release Runbook and Durable Memory

This file is the durable operating memory for agents that prepare, execute, resume, or verify releases of AIEngineeringStandard. Read it at the start of every release-related task, including after a context reset. It complements the canonical rules in `AGENTS.md` and `docs/releases/README.md`; it does not override branch protection or grant publication authorization.

## 1. Capability discovery: verify, do not assume

Before requesting user intervention, inventory the capabilities actually exposed by the current host:

- Workspace/sandbox shell, filesystem, Git, Python, package build tools, and network availability.
- GitHub read and write actions separately: fetch files, inspect commits/branches, create a working branch/PR, update refs, create tags/releases, inspect Actions runs/logs/artifacts.
- Authentication and authorization for this specific repository and for the `pypi` publishing environment.
- Direct package index visibility and the ability to verify the exact published version.
- Repository-owned release scripts and workflow fallbacks.

Distinguish a tool method not being exposed from missing authentication, app installation, repository selection, or account permission. Read access does not prove write access. A previous session's capability does not prove that the current session can use it. Do not claim an action was executed unless the tool result or durable remote state proves it.

Use the repository's supported path, not an invented substitute. For this project, the canonical release path is `python3 scripts/release/check_release.py` followed by `python3 scripts/release/publish_release.py` from an exact, clean local `main` checkout. If that environment is unavailable, inspect the actual script, workflow trigger, permissions, and outputs before selecting a bounded fallback. Never misuse a branch ref operation as a tag operation.

## 2. Reconcile durable state before continuing

Conversation history is not authoritative for current state. Verify the following independently for the exact version and commit:

| Stage | Evidence required |
| --- | --- |
| Source prepared | `VERSION`, `core/common/environment.py`, branch name, clean tree, and exact `HEAD == origin/main` SHA |
| Local preflight | Fresh output from `scripts/release/check_release.py` on that exact source |
| CI and runtime evidence | Relevant Actions run tied to the exact SHA; inspect conclusions, failed/skipped jobs, and logs. Record runtime checks as `PASS`, `FAIL`, `UNTESTED`, `UNSUPPORTED`, `SKIPPED`, or `BLOCKED` only when supported by evidence |
| Git tag | Remote tag exists and its peeled/target commit equals the approved source SHA |
| GitHub Release | Release exists for the exact tag; inspect URL, draft/prerelease status, and expected assets |
| Package publication | Package index reports the exact version; inspect built distribution artifacts and publishing workflow result |
| Post-publication | Confirm tag, release, workflow, artifacts, and package independently; preserve evidence links and any remaining gap |

Before creating anything, check whether the tag, Release, and package version already exist. If a stage is already complete, verify its identity and resume from the first incomplete stage. Never force-move or overwrite an immutable release tag to recover from a partial failure.

## 3. Approval boundary

Preparation and publication are separate operations.

- Inspection, editing a branch, running tests, validating a release candidate, and preparing a plan do not publish the package.
- Pushing a release tag triggers the public publishing workflow. Creating a public GitHub Release and publishing to PyPI are externally visible side effects.
- Require explicit user authorization for the exact release/publication task before initiating those side effects, unless the user has already clearly authorized those exact actions in the current task. A general “continue” or approval to improve release memory is not itself authorization to publish a specific version.
- Never expose tokens or credentials in files, logs, artifacts, or mission inputs.

## 4. Canonical execution sequence

1. Read this runbook, `AGENTS.md`, `docs/releases/README.md`, `scripts/release/check_release.py`, `scripts/release/publish_release.py`, and `.github/workflows/publish-package.yml`.
2. Verify `main` is the intended source, the working tree is clean, local `HEAD` exactly matches refreshed `origin/main`, and the release tag does not already exist locally or remotely.
3. Confirm `VERSION` and the runtime's reported version agree.
4. Run `python3 scripts/release/check_release.py`. Do not weaken checks to obtain a pass.
5. Verify CI and any required runtime conformance evidence for the same source SHA. A green CI run alone is not proof of all runtime behavior. Unavailable evidence remains explicitly incomplete.
6. Present the exact version, source SHA, completed checks, known limitations, expected public side effects, and rollback/recovery implications; obtain explicit approval when required.
7. Run `python3 scripts/release/publish_release.py` only in an environment that has the required GitHub CLI/authentication and exact checked-out source. The script pushes the annotated tag and creates the canonical GitHub Release. The tag-triggered workflow validates and builds distributions, waits for that Release to exist, attaches artifacts, and publishes to PyPI.
8. Verify every stage independently. Report preparation, tag creation, GitHub Release, Actions, PyPI publication, and post-publication checks separately.

## 5. Failure recovery matrix

| Observed state | Recovery |
| --- | --- |
| Preflight fails | Stop. Report the exact failing check; repair the cause and rerun validation. Do not publish. |
| Tag push fails | Verify remote refs and local tag state before retrying. The script removes its local tag after a push failure, but the remote must still be checked. |
| Tag exists but Release is absent | Verify the tag points to the intended approved SHA. Inspect the script/workflow result. Create the missing Release only through an authorized, documented recovery; do not blindly rerun the whole script or recreate the tag. |
| Release exists but workflow is still running | Inspect the exact run, job state, and logs. Wait for terminal state or retry only the failed/retry-safe step. |
| PyPI publication fails after tag/Release exists | Keep the existing tag immutable. Inspect the publishing logs, environment/trusted-publishing configuration, and PyPI state; retry the workflow only when safe. |
| PyPI reports the version already exists | Verify the published files and version identity. Do not assume they match the intended source merely because the version number exists. |
| Any state is ambiguous | Stop side effects; gather direct GitHub/PyPI evidence and report the ambiguity. Do not infer success or delete/force-update public state. |

## 6. Release record template

For each release, maintain a dated record in the relevant release note or task report:

- Version:
- Approved source SHA:
- Preflight result:
- CI run URL and conclusion:
- Runtime conformance evidence and explicit gaps:
- Remote tag URL and target SHA:
- GitHub Release URL and asset list:
- Publishing workflow URL and conclusion:
- Package index URL and published version:
- Remaining blockers / recovery action:
- Approval evidence for public side effects:

Do not store secrets, personal credentials, or transient tokens in this record.

## 7. Current-session rule

At each session start, refresh the facts from GitHub and PyPI. This document records procedure, not a claim that any specific release is currently published. For the present `v2.2.1` task, prior evidence indicated local preflight and main CI passed, while runtime failure-recovery evidence remained `UNTESTED`; the remote tag and GitHub Release appeared absent and PyPI's latest version was `2.2.0`. Treat those as historical leads only and re-check them before acting.
