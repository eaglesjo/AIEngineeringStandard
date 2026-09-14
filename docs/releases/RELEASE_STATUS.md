# Release Status

Release target: `2.0.0`.

Status: **public release candidate**. The validated 2.0.0 candidate has been promoted to the public repository and is undergoing the final public audit. The `v2.0.0` tag and GitHub Release remain a separate publication authorization step.

## Final audit focus

- canonical repository architecture and policy profiles
- dependency and layer-boundary validation
- environment and resource detection
- multilingual runtime resource completeness and semantic parity
- installer lifecycle behavior across supported platforms
- LLM and Vision CPU smoke validation
- Google Colab runtime and notebook validation
- deterministic RAG regression and quality gates
- executable agent-conformance validation
- dependency alignment and isolated real pip resolver validation
- AI code-quality verification
- AI/LLM evaluation
- evidence provenance and traceability
- data/model reproducibility

## Release invariants

- Preserve historical tags and commits.
- Promote only an exact validated development revision.
- Keep development and validation responsibilities in `codingStandard-dev`.
- Treat the public repository as the distribution and audit surface.
- Do not describe unavailable runtime evidence as passed.
- Create the public tag and release only after the final audit and release authorization are complete.

## Publication gate

`v2.0.0` tag/release: **NOT AUTHORIZED YET**.
