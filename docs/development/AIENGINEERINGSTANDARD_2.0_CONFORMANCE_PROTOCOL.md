# AIEngineeringStandard 2.0 Conformance Protocol

## Purpose

This protocol defines how an AI agent is promoted from `UNTESTED` to an evidence-backed conformance status. File presence or documentation claims are not runtime conformance evidence.

## Test stages

1. **Instruction discovery** — verify the agent discovers the declared project instruction contract.
2. **Skill discovery** — verify the portable Skill location is discoverable.
3. **Skill loading** — load a deterministic, non-executable fixture Skill and verify its declared behavior is available to the agent.
4. **Plugin capability discovery** — verify the declared Agent Plugin contract can be discovered without executing untrusted code.
5. **MCP capability discovery** — verify the declared MCP boundary and capability metadata.
6. **Permission enforcement** — attempt controlled operations against an explicit permission matrix and verify denied operations remain denied.
7. **Controlled task execution** — execute a deterministic task whose expected result is known.
8. **Validation/reporting** — verify the result is checked against the expected output and emitted in the machine-readable conformance schema.
9. **Failure recovery** — inject a deterministic recoverable failure and verify bounded recovery behavior.
10. **Evidence reporting** — retain runtime version, test timestamp, test inputs, observed result, and evidence references.

## Safety boundary

The conformance runner MUST NOT execute arbitrary Skill, Plugin, or MCP code. Static checks inspect metadata, paths, schemas, and deterministic fixtures only. Runtime tests must execute in an explicitly controlled environment with bounded permissions.

## Codex first implementation

Codex is the first P0 runtime target. The initial test fixture uses the repository's canonical `AGENTS.md` instruction contract and `.agents/skills/` portable Skill location.

The first runtime campaign should record:

- Codex runtime/version identifier
- repository commit under test
- instruction discovery observation
- Skill discovery observation
- Skill loading observation
- permission test observations
- deterministic task output
- failure-recovery observation
- generated conformance result

No `PASS` status may be assigned from static inspection alone.

## Promotion rules

- `UNTESTED`: no runtime evidence for the required stage.
- `PASS`: required stages pass with objective evidence.
- `PARTIAL`: useful support exists but one or more contract capabilities have documented limitations.
- `ADAPTER`: conformance is achieved through a documented adapter boundary.
- `UNSUPPORTED`: the agent cannot satisfy the required contract.
- `FAIL`: a deterministic contract check is violated; this is primarily a validation/CI state and must not be silently converted into support.

## Reproducibility

Runtime evidence must be tied to an immutable repository revision and a recorded agent/runtime version. Mutable branch names alone are insufficient evidence. Tests should be deterministic and safe to rerun.

## Result artifact

The machine-readable output MUST conform to `core/validation/conformance-result.schema.json`. The committed Codex static expectation is under `tests/validation/fixtures/conformance/codex-static.expected.json` and is explicitly not runtime evidence.
