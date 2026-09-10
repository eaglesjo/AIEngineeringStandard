#!/usr/bin/env python3
"""Guardrails for conservative mapping from Codex JSONL to 2.0 evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "validation"))

from run_runtime_conformance import parse_codex_jsonl  # noqa: E402


def event(event_type: str, item: dict | None = None, **extra: object) -> str:
    payload: dict[str, object] = {"type": event_type, **extra}
    if item is not None:
        payload["item"] = item
    return json.dumps(payload)


def ids(observations: list[dict]) -> set[str]:
    return {observation["id"] for observation in observations}


def main() -> int:
    observations, warnings, permission_denial = parse_codex_jsonl(
        event(
            "item.completed",
            {
                "type": "mcp_tool_call",
                "server": "fixture-mcp",
                "name": "fixture.read",
                "status": "completed",
            },
        )
    )
    observed = ids(observations)
    assert not warnings, warnings
    assert not permission_denial
    assert "codex-mcp-tool-call" in observed
    assert "codex-skill-file-access" not in observed
    assert "codex-permission-denial" not in observed

    # The parser intentionally recognizes canonical .agents/skills/ access as
    # useful evidence, while keeping it distinct from first-class Skill load.
    observations, warnings, permission_denial = parse_codex_jsonl(
        event(
            "item.completed",
            {
                "type": "command_execution",
                "command": "cat .agents/skills/portable-skill/SKILL.md",
                "status": "completed",
                "exit_code": 0,
            },
        )
    )
    observed = ids(observations)
    assert not warnings, warnings
    assert not permission_denial
    assert "codex-command-execution" in observed
    assert "codex-skill-file-access" in observed
    assert "codex-permission-denial" not in observed

    observations, warnings, permission_denial = parse_codex_jsonl(
        event(
            "item.completed",
            {
                "type": "command_execution",
                "command": "printf 'permission denied is only prompt text'",
                "status": "completed",
                "exit_code": 0,
            },
        )
    )
    assert not warnings, warnings
    assert not permission_denial
    assert "codex-permission-denial" not in ids(observations)

    observations, warnings, permission_denial = parse_codex_jsonl(
        event(
            "item.completed",
            {
                "type": "command_execution",
                "command": "cat protected-permission-target.txt",
                "status": "failed",
                "exit_code": 1,
                "aggregated_output": "permission denied: protected file is outside granted permissions",
            },
        )
    )
    assert not warnings, warnings
    assert permission_denial
    assert "codex-permission-denial" in ids(observations)

    print("Codex evidence mapping guardrail tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
