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

## v2.1 architecture contract

The canonical multi-agent model is defined by `core/contracts/2.1/`. Runtime adapters must map their native concepts into these contracts and must not redefine their semantics. A Work Unit owns the trace boundary; Handoffs carry explicit provenance; Evaluation cannot silently convert unavailable evidence into PASS; Acceptance is downstream of Evaluation.

## Release rules

A release is created from this repository only. Run `python3 scripts/release/check_release.py` from an exact, clean `main` checkout, then use `python3 scripts/release/publish_release.py` to create the annotated tag and GitHub Release. GitHub Actions is not part of the release architecture. Never promote source from another repository.

## Agent/tool adapters

Root and tool-specific instruction files are adapters to this contract. They must not introduce a conflicting canonical policy.
