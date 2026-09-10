---
name: aies-portable-skill-fixture
description: Minimal fixture used to validate the AIEngineeringStandard 2.0 portable Skill contract.
license: MIT
---

# AIES Portable Skill Fixture

Use this fixture only to validate Skill discovery and loading. It intentionally performs no tool calls, filesystem writes, network access, or secret handling.

## Contract checks

- The entry point is `SKILL.md`.
- The Skill is vendor-neutral.
- The Skill does not grant runtime permissions.
- The Skill can be validated without executing arbitrary code.
