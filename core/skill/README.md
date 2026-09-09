# Skill Standard Layer

`core/skill/` defines the portable Agent Skill contract for AIEngineeringStandard 2.0.

## Normative principles

1. Prefer the open `SKILL.md` format.
2. Prefer `.agents/skills/` as the portable project-level discovery location where the runtime supports it.
3. Keep Skill instructions vendor-neutral.
4. Declare executable content and security expectations.
5. Preserve provenance and version information where packaging permits it.
6. Do not create per-agent copies of identical Skill content unless an adapter is genuinely required.

Existing 1.x Skills are not moved or duplicated by M1. Migration happens only after the canonical contract and validation are established.
