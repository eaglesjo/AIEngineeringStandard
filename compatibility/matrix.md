# AIEngineeringStandard 2.0 Agent Compatibility Matrix

This matrix is the human-readable view of `compatibility/agents.json`.

## Status policy

- **PASS** — the capability has been exercised by an objective conformance test and evidence is recorded.
- **PARTIAL** — the capability works with documented limitations and evidence.
- **ADAPTER** — compatibility is provided through a documented adapter rather than native support.
- **UNTESTED** — compatibility is planned or structurally plausible, but no conformance evidence has been accepted yet.
- **UNSUPPORTED** — the capability is known not to be available or cannot satisfy the 2.0 contract.

> **Rule:** An adapter file, documentation page, or repository convention alone never earns `PASS`.

## P0 — must support

| Agent | Instructions | Skills | Plugins | MCP | Sub-agent | Execution | Overall |
|---|---|---|---|---|---|---|---|
| OpenAI Codex | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| Claude Code | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| GitHub Copilot | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| Gemini / Antigravity | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| Google Colab Gemini Agent | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| Cursor | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| OpenCode | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| Roo Code | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |

## P1 — actively support

| Agent | Instructions | Skills | Plugins | MCP | Sub-agent | Execution | Overall |
|---|---|---|---|---|---|---|---|
| Cline | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| Continue | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| Windsurf | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |
| Amazon Q Developer | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED |

## P2 — compatibility / adapter coverage

| Agent | Planned status |
|---|---|
| Aider | UNTESTED |
| Amp | UNTESTED |
| Goose | UNTESTED |
| Devin | UNTESTED |
| JetBrains Junie | UNTESTED |
| Augment | UNTESTED |
| Cortex Code | UNTESTED |
| Crush | UNTESTED |
| CodeBuddy | UNTESTED |
| Command Code | UNTESTED |
| IBM Bob | UNTESTED |

## Conformance evidence model

Each promoted capability should be backed by a machine-readable conformance result using `core/validation/conformance-result.schema.json`.

Minimum test stages:

1. Instruction discovery
2. Skill discovery
3. Skill loading
4. Plugin capability discovery
5. MCP capability discovery
6. Permission enforcement
7. Controlled task execution
8. Validation/reporting
9. Failure recovery
10. Evidence reporting

Runtime versions should be recorded when a test is executed. Results are tied to the tested runtime and should not be generalized indefinitely across future agent releases.

## Promotion rule

A capability moves from `UNTESTED` to `PASS`, `PARTIAL`, or `UNSUPPORTED` only after a conformance test records evidence. `ADAPTER` is reserved for compatibility intentionally supplied through an adapter boundary.
