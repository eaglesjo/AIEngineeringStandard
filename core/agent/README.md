# Agent Standard Layer

AIEngineeringStandard 2.0 introduces `core/agent/` as the normative layer for agent execution contracts.

This directory defines vendor-neutral concepts only. Platform-specific behavior belongs under `agents/` and must remain a thin adapter over the portable contracts.

## Initial contract surface

- agent identity and capability declaration;
- instruction and policy discovery;
- Skill and Plugin capability boundaries;
- tool and MCP permission boundaries;
- delegation/sub-agent contracts;
- execution evidence and result reporting.

The 2.0-M1 schemas are intentionally additive. Existing 1.x rules and adapters remain authoritative until a migration milestone explicitly replaces them.
