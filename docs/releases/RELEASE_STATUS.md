# Release Status

Release development target: `2.0.0`.

Status: **pre-release preparation**. `codingStandard-dev` main is the implementation and validation surface for the release candidate. A validated result may be promoted to `eaglesjo/AIEngineeringStandard`; no public release tag is created by this repository state alone.

## Validation focus

- canonical repository architecture and policy profile validation
- repository dependency and layer-boundary validation
- environment contract and resource detection validation
- multilingual runtime resource completeness, semantic policy parity, and runtime/documentation consistency
- installer dry-run, merge/overwrite/skip, manifest, update, obsolete-file reconciliation, and protected uninstall behavior
- LLM and Vision CPU memory smoke tests
- Google Colab runtime and notebook validation
- deterministic RAG regression and quality-gate coverage
- executable agent-conformance schema/policy validation
- dependency compatibility policy and deterministic resolver validation
- isolated real pip resolver integration validation
- final release-gate validation on the exact release-candidate commit

## Release invariants

- Preserve all historical tags and commits, including the existing 1.x history.
- Do not move AI Engineering Standard source or release responsibilities back into `codingStandard-private`.
- Implement and validate release changes in `codingStandard-dev` before promotion.
- Promote only an exact validated development commit to `eaglesjo/AIEngineeringStandard`.
- Perform a second full audit on the final public candidate before creating `v2.0.0`.
- Do not describe unavailable runtime evidence as passed; retain `UNTESTED` / `SKIPPED` where applicable.

## Current gate

`v2.0.0` tag/release: **NOT AUTHORIZED YET**.

Required sequence: preparation → development CI → pre-promotion audit → promotion → final public full audit → release authorization → tag/release.
