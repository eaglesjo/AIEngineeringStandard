# Portable Agent Skill Contract — 2.0

This document defines the AIEngineeringStandard contract for portable Agent Skills.

## 1. Canonical format

A portable Skill is a directory whose entry point is `SKILL.md`. The entry point contains YAML frontmatter followed by human-readable instructions.

The preferred project-level discovery location is:

```text
.agents/skills/<skill-name>/SKILL.md
```

When an agent has a native discovery location, an adapter may expose the same canonical Skill without copying or forking its content.

## 2. Required properties

A portable Skill MUST:

- have a stable directory name;
- contain exactly one canonical `SKILL.md` entry point for that Skill;
- state what capability/workflow it provides;
- define safe operating boundaries when tools or executable resources are involved;
- avoid embedding secrets, credentials, or environment-specific private data;
- remain vendor-neutral unless the Skill is explicitly an adapter Skill.

## 3. Optional resources

A Skill MAY contain `references/`, `scripts/`, `assets/`, or other resources required by the workflow.

Executable resources MUST be treated as code, not trusted merely because they are distributed inside a Skill. Validation SHOULD inspect them for unsafe behavior and unexpected network, filesystem, credential, or command access.

## 4. Source-of-truth rule

The same Skill content MUST NOT be duplicated across agent-specific directories solely to satisfy discovery. If an adapter is required, it MUST point to, package, or project the canonical Skill while preserving a single authoritative source.

## 5. Versioning

Skill compatibility follows the AIEngineeringStandard major version. A Skill may declare its own version when independent lifecycle management is useful.

Breaking changes to the Skill contract require an AIEngineeringStandard major-version change unless a compatibility-preserving extension is possible.

## 6. Security and provenance

Consumers SHOULD record the Skill source, version or commit where available, and validation result. Untrusted Skills MUST NOT be treated as privileged instructions.

A Skill does not grant permission to access tools, files, networks, secrets, or external systems. Those permissions belong to the runtime, agent, Plugin, or MCP security boundary.
