# AIEngineeringStandard Agent Contract

## Repository role

This repository is the canonical development, validation, and release source for AI Engineering Standard. Do not assume or reference a separate private, development, staging, promotion, or export repository.

## Before changing code

1. Read `README.md` and the applicable files under `docs/development/` and `docs/releases/`.
2. Inspect `profiles/project.json` and the relevant architecture/policy profiles.
3. Preserve the canonical directory layout.
4. Run the narrowest relevant validation while developing, then the full validation before merge or release.
5. For v2.1 contract changes, preserve the canonical Agent → Role → Contract → Work Unit → Handoff → Evidence → Evaluation → Acceptance model.

## Source of truth

- `VERSION` is the release version.
- `core/common/environment.py` must agree with `VERSION`.
- `i18n/languages.json` is the locale catalog.
- `compatibility/agents.json` is the agent compatibility catalog.
- Git history, tags, and GitHub Releases are the release provenance.

## Development rules

- Work in a feature/fix/docs branch; keep `main` releasable. The repository may temporarily use a development branch, but the final remote branch set remains `main` only.
- Do not commit secrets, credentials, local runtime state, generated caches, or machine-specific paths.
- Do not weaken validation to make a release pass.
- Keep unavailable runtime evidence explicitly `UNTESTED`, `UNSUPPORTED`, `SKIPPED`, or `BLOCKED`.
- Prefer small, auditable commits.
- Update tests and documentation when a contract changes.

## CI and execution

- GitHub Actions is part of the repository validation architecture.
- `.github/workflows/ci.yml` is the canonical automated CI entry point.
- Repository execution follows `core/runtime/execution/OPERATING_POLICY.md` and `core/runtime/execution/mission.schema.json`.
- CI uses least-privilege read permissions and immutable repository state.
- Prefer sandbox/local execution for iterative development; use Actions for bounded automated validation or remote execution when appropriate.
- A green workflow is not by itself acceptance evidence; relevant outputs and source identity must be verified.
- Do not add project secrets to workflow source, logs, artifacts, or mission payloads.
- Temporary Actions state must be task-owned and cleaned up after terminal use.
- When execution is lost or context is reset, recover from durable Git/Actions state before conversation reconstruction.

## v2.1 architecture contract

The canonical multi-agent model is defined by `core/contracts/2.1/`. Runtime adapters must map their native concepts into these contracts and must not redefine their semantics. A Work Unit owns the trace boundary; Handoffs carry explicit provenance; Evaluation cannot silently convert unavailable evidence into PASS; Acceptance is downstream of Evaluation.

## Release rules

A release is created from this repository only. Run `python3 scripts/release/check_release.py` from an exact, clean `main` checkout, then use `python3 scripts/release/publish_release.py` to create the annotated tag and GitHub Release. Never promote source from another repository.

## Connected tool capability discovery and fallback

- At the start of repository work, inventory the capabilities actually available in the current host: sandbox execution, connected GitHub read/write operations, Git object/ref operations, workflow dispatch, Actions logs/artifacts, and release/package status checks. Distinguish a missing operation in the currently exposed tool list from missing installation, repository authorization, or account permission; do not infer one from another.
- In the documented ChatGPT Web path, use the GitHub Plugin together with the ChatGPT Codex Connector GitHub App when both are available for the target repository. Setup references: [ChatGPT Plugins](https://chatgpt.com/plugins) and [ChatGPT Codex Connector GitHub App](https://github.com/apps/chatgpt-codex-connector). The user must complete any required sign-in, installation, repository selection, and organization-admin approval. Never claim a connector is installed, authorized, or able to access a repository until the active connection and actual repository capabilities are verified.
- Treat the two connections as complementary, not interchangeable: the ChatGPT-side GitHub connection exposes the repository actions available to the conversation, while the GitHub App installation grants repository-scoped access to the Codex Connector path. Exact UI labels and availability can change; follow the current product screens and least-privilege repository selection. If either connection is unavailable, inspect the capabilities actually exposed and continue with supported paths instead of assuming the setup is complete.
- README setup instructions must identify both connection steps, link to their official setup pages, explain repository access selection and possible organization approval, and tell users to verify access by asking the agent to inspect the intended repository.
- Sandbox-first: recover the exact repository state and verify its immutable commit SHA before editing or executing commands. Inventory existing sandbox capabilities before installing tools or moving work to Actions.
- Do not conclude that an operation is impossible after checking only one connector action. Inspect repository-owned scripts, documented procedures, workflows, and available connected capabilities first. Never misuse a branch-only ref operation to create a tag or silently substitute a different operation.
- If a required GitHub operation is not directly exposed, use the smallest safe repository-supported fallback that actually exists: an existing release script from the required clean checkout, or a bounded GitHub Actions mission/workflow when its trigger, inputs, permissions, and outputs support the task. Do not invent workflow names, dispatch capabilities, credentials, or shell access. If no supported path exists, report the exact capability blocker and the alternatives verified.
- Every fallback must be bounded to an immutable source SHA and explicit purpose, inputs, operations, permissions, expected outputs, and verification. Inspect run conclusions, logs, resulting refs/releases/artifacts, and package publication status before claiming success. A green workflow alone is not proof that the requested release was published.
- For releases, follow the repository's Release rules and scripts first: run `scripts/release/check_release.py` from an exact clean `main` checkout, then `scripts/release/publish_release.py`. If the current environment cannot run these scripts, inspect the release workflow and available GitHub/Codex/Actions paths before declaring a blocker or asking the user to publish manually.
- Report separately what was prepared, what was actually published, and what post-publication checks were verified. Never claim a tag, GitHub Release, or package publication without direct evidence.

## Agent/tool adapters

Root and tool-specific instruction files are adapters to this contract. They must not introduce a conflicting canonical policy.

## Sandbox-first agent execution contract

This contract is mandatory for repository work initiated from chat or another agent host.

1. **Start with the execution environment that already exists.** Inventory the current host's shell/code workspace, filesystem, Git, runtimes, package tools, and connected GitHub/Actions operations before asking for user-side setup. Do not assume that the absence of a Codex CLI or a dedicated GitHub action means no execution path exists.
2. **Materialize exact source before engineering work.** Resolve the intended branch or PR to an immutable commit SHA. Inspect any surviving workspace first. Prefer clone/fetch when network access works; otherwise use an available connected repository read or a bounded, checksummed artifact/Actions transport. Verify the checked-out or materialized tree corresponds to the expected SHA before editing, building, or testing.
3. **Keep the user's computer outside the normal workflow.** Do not ask the user to install a local CLI, share a shell, or weaken host isolation merely to unblock ordinary repository development. Only propose a local setup when the task genuinely requires a capability unavailable in supported chat/sandbox paths and alternatives have been examined.
4. **Discover actual capabilities, not assumptions.** Distinguish a missing tool method from missing authentication, installation, repository authorization, or account permission. Inspect available read/write Git operations, ref/tag operations, workflow triggers, logs, artifacts, and repository-owned scripts. Do not infer write capability from read access or infer impossibility from one missing operation.
5. **Use the smallest safe supported path.** Prefer the normal sandbox for editing/build/test/debug. If an operation is unavailable there, inspect project scripts and existing workflows, then use a bounded Actions mission or connected GitHub operation only if its trigger, inputs, permissions, and outputs actually support the task. Never invent a dispatch endpoint, credential, workflow, or shell capability. Do not misuse a branch-only ref operation to create a tag.
6. **Bound every remote mission.** Pin the source SHA and state the purpose, exact inputs, permitted operations, minimum permissions, expected outputs, integrity checks, and terminal state. Do not run untrusted code with privileged credentials. Preserve source identity and inspect logs, results, refs, artifacts, and checksums before consuming mission outputs.
7. **Release procedures are authoritative.** For a release, inspect and follow `docs/releases/README.md`, `scripts/release/check_release.py`, `scripts/release/publish_release.py`, and the package-publishing workflow. Require a clean checkout of the exact current `main`, pass preflight, and preserve branch protections and validation. Never silently replace the official procedure with a weaker shortcut.
8. **Recover before escalating.** If a command or connector call fails, inspect the actual error and current durable GitHub state. Retry only when the failure is plausibly transient and retry is safe; otherwise select a different exact supported transport or report the concrete blocker and verified alternatives.
9. **Report evidence by stage.** Separate preparation, source validation, tag creation, GitHub Release creation, package publication, and post-publication verification. A green CI run, an existing tag, or a created release alone does not prove all release stages succeeded. Mark unexecuted checks as blocked/incomplete and include direct evidence links.
10. **Fallback must not become user burden by default.** Do not stop at “this chat has no shell” or immediately ask the user to perform commands. First inventory the real sandbox, connected operations, repository scripts, and viable bounded Actions paths. Ask for user intervention only when a required authorization/approval or an unsupported capability genuinely cannot be supplied through those paths.

This contract complements the release and validation rules above; it does not authorize bypassing branch protection, repository policy, package provenance, or required review.
