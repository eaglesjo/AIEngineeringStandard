#!/usr/bin/env python3
"""Focused edge-case tests for the bounded Codex JSONL parser."""
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


def results(observations: list[dict]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for observation in observations:
        grouped.setdefault(observation["id"], []).append(observation["result"])
    return grouped


def main() -> int:
    valid = "\n".join(
        [
            event("thread.started"),
            event("item.completed", {"type": "command_execution", "command": "cat .agents/skills/portable-skill/SKILL.md"}),
            event("item.completed", {"type": "mcp_tool_call"}),
            event("item.completed", {"type": "file_change"}),
            event("turn.completed"),
        ]
    )
    observations, warnings = parse_codex_jsonl(valid)
    grouped = results(observations)
    assert not warnings, warnings
    assert grouped["codex-jsonl-event-stream"] == ["OBSERVED"]
    assert grouped["codex-command-execution"] == ["OBSERVED"]
    assert grouped["codex-skill-file-access"] == ["OBSERVED"]
    assert grouped["codex-mcp-tool-call"] == ["OBSERVED"]
    assert grouped["codex-file-change"] == ["OBSERVED"]

    malformed = "{not-json}\n" + event("turn.completed")
    observations, warnings = parse_codex_jsonl(malformed)
    assert any("non-JSON output ignored" in warning for warning in warnings)
    assert results(observations)["codex-jsonl-event-stream"] == ["OBSERVED"]

    unknown = event("future.event", answer="do not infer")
    observations, warnings = parse_codex_jsonl(unknown)
    assert not observations
    assert any("unknown event type" in warning for warning in warnings)

    top_level_error = event("error", message="stream failure")
    observations, warnings = parse_codex_jsonl(top_level_error)
    assert not warnings
    assert results(observations)["codex-stream-error"] == ["OBSERVED"]

    item_error = event("item.completed", {"type": "error", "message": "recoverable item error"})
    observations, warnings = parse_codex_jsonl(item_error)
    assert not warnings
    assert not observations, "item-level errors must not be promoted to fatal stream errors"

    malformed_item = event("item.completed")
    observations, warnings = parse_codex_jsonl(malformed_item)
    assert not observations
    assert any("has no object item" in warning for warning in warnings)

    print("Codex JSONL parser edge-case tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
