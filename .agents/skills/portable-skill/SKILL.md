---
name: aies-portable-skill-fixture
description: Minimal portable Skill used to validate AIEngineeringStandard 2.0 Skill discovery and loading.
license: MIT
---

# AIES Portable Skill Fixture

Use this Skill only for deterministic validation of the portable Skill contract.

## Contract checks

- The entry point is `SKILL.md`.
- The Skill is vendor-neutral.
- The Skill does not grant runtime permissions.
- The Skill performs no tool calls, filesystem writes, network access, or secret handling.
- The Skill can be validated without executing arbitrary code.

## Safety boundary

This Skill is instructional content only. Runtime permissions remain controlled by the agent, Plugin, MCP, and execution environment.
