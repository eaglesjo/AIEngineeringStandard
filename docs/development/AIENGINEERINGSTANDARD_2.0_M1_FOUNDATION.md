# AIEngineeringStandard 2.0-M1 Foundation

Status: **In progress**

Baseline: **1.17.2**

This milestone establishes the first additive 2.0 contracts without removing or relocating working 1.x integrations.

## Baseline audit snapshot

The 1.17.2 repository already contains:

- platform instruction/adapters for multiple AI clients;
- `core/common` Skill and agent guidance;
- project, architecture and policy profiles;
- existing validation scripts for structure, domains, profiles, agent routing and multilingual resources;
- dedicated Colab, installer, integration and validation test areas.

Therefore M1 must extend these surfaces rather than create a parallel replacement system.

## M1 foundation added

- `core/agent/` — vendor-neutral agent contract boundary.
- `core/skill/` — portable Skill contract boundary.
- `core/plugin/` — Agent Plugin 1.0 packaging boundary.
- `core/mcp/` — MCP integration and trust boundary.
- `core/validation/` — machine-readable conformance contract.
- `profiles/agent/` — agent-aware profile boundary.
- `compatibility/agents.json` — compatibility catalog schema.

## Source-of-truth rule

1. Existing 1.x rules remain authoritative until a migration milestone changes them.
2. Portable 2.0 contracts are defined under `core/`.
3. Runtime-specific adapters belong under `agents/` and should remain thin.
4. Reusable Skills belong in the canonical portable layer and must not be copied per agent without a technical reason.
5. Compatibility claims require evidence; file presence alone is insufficient.

## Next M1 work

1. Add deterministic schema validation to the existing validation suite.
2. Build the first portable Skill fixture from the existing common Skill without duplicating its authoritative content.
3. Add the first conformance test fixture and result artifact.
4. Add the initial P0 compatibility catalog entries as `UNTESTED` until real validation evidence exists.
5. Define the 2.0 security/provenance contract before Plugin/MCP implementation.

## Migration constraint

No 1.x adapter is removed in M1. No existing public installation path is intentionally broken by the foundation work.
