---
name: ai-engineering-standard
description: Apply the repository's canonical AI engineering standards before implementation, validation, and release changes.
---

# AI Engineering Standard Skill

Use this Skill when a task changes engineering policy, agent behavior, AI/ML runtime behavior, validation, installation, or release behavior.

## Required behavior

1. Read the repository-level `AGENTS.md`.
2. Inspect the applicable architecture and policy profiles.
3. Prefer existing canonical contracts over introducing parallel rules.
4. Run focused validation during development.
5. Run the full validation gates before merge or release.
6. Preserve explicit uncertainty states such as `UNTESTED` and `UNSUPPORTED`.

## Release boundary

This repository is the sole development and release source. Do not introduce or rely on a separate promotion repository.
