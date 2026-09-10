#!/usr/bin/env python3
"""Validate the portable Agent Skill contract without executing Skill code."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "tests" / "validation" / "fixtures" / "portable-skill" / "SKILL.md"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> int:
    if not SKILL.is_file():
        fail(f"portable Skill fixture missing: {SKILL}")

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must begin with YAML frontmatter")

    end = text.find("\n---\n", 4)
    if end < 0:
        fail("SKILL.md frontmatter is not closed")

    frontmatter = text[4:end]
    body = text[end + len("\n---\n"):].strip()
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            fail(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    for required in ("name", "description", "license"):
        if not fields.get(required):
            fail(f"SKILL.md frontmatter missing: {required}")
    if not NAME_RE.fullmatch(fields["name"]):
        fail(f"invalid Skill name: {fields['name']!r}")
    if len(fields["description"]) < 10:
        fail("Skill description is too short")
    if not body:
        fail("SKILL.md body must not be empty")

    prohibited = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GITHUB_TOKEN", "AWS_SECRET_ACCESS_KEY")
    for token in prohibited:
        if token in text:
            fail(f"secret-like token found in Skill fixture: {token}")

    print("Portable Agent Skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
