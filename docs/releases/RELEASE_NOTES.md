# 2.0.0 Release Notes

AI Engineering Standard 2.0.0 establishes the repository's agent-engineering and validation contracts as a cohesive, machine-readable release surface. It preserves the historical 1.x line while introducing explicit 2.0 architecture, conformance, provenance, and dependency-compatibility controls.

## Highlights

### Agent and Skill engineering

- Add a canonical project-level `AGENTS.md` entrypoint and portable Skill contract.
- Add agent profiles and documented integration paths for Codex, Claude Code, Gemini/Antigravity, Copilot, Cursor, Windsurf, Cline, Continue, Junie, Amazon Q, Aider, and related tooling.
- Add explicit plugin and MCP capability documentation and discovery contracts.

### Architecture and policy

- Add machine-readable project, architecture, policy, and agent profiles.
- Make layer boundaries, dependency direction, runtime assumptions, and repository-wide policy explicit and machine-validatable.
- Add dependency compatibility policy anchored to the developer-selected library/version.
- Add deterministic dependency alignment resolution and isolated real pip resolver integration tests.

### Executable conformance

- Add conformance result and evidence schemas with explicit `PASS`, `PARTIAL`, `ADAPTER`, `UNTESTED`, `UNSUPPORTED`, and `FAIL` outcomes.
- Add mandatory checks for instruction/Skill discovery and loading, plugin/MCP capability, permissions, task execution, validation, failure recovery, and evidence reporting.
- Add security/provenance contracts and protected-operation integrity checks.
- Add Codex runtime adapter and bounded runtime conformance execution when the Codex CLI is available.

### Validation and reproducibility

- Expand the repository validation gate to cover the new 2.0 schemas, conformance fixtures, adapters, dependency alignment, and evidence mapping.
- Preserve architecture, i18n, installer, Colab, RAG, LLM, Vision, and CPU smoke validation already established by the project.
- Keep unavailable runtime capabilities explicitly marked as `UNTESTED` / `SKIPPED` rather than treating absence as success.

### Release boundary

- Formalize the release flow:

  `codingStandard-private → codingStandard-dev → AIEngineeringStandard`

- `codingStandard-private` is the Luna/internal continuity surface.
- `codingStandard-dev` is the implementation and validation surface.
- `AIEngineeringStandard` is the public release surface.
- Public release must be created only from an exact validated public commit after the final audit gate.

## Validation evidence

The dependency-compatibility 2.0 scope was validated in development CI and promoted to the public repository. Final public conformance run `34683162767` completed successfully for all applicable executable checks. The live Codex CLI steps were skipped because the CLI was unavailable in the runner; this is an explicit evidence limitation, not a live-runtime pass.

## Release gate for v2.0.0

These notes describe the intended 2.0.0 release. The `v2.0.0` tag and GitHub Release remain blocked until the release-preparation changes pass development CI, are promoted to the public repository, and the final public candidate passes the required second full audit.
