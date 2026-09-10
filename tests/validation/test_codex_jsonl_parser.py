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
    observations = parse_codex_jsonl(valid)
    grouped = results(observations)
    assert grouped["codex-jsonl-event-stream"] == ["OBSERVED"]
    assert grouped["codex-command-execution"] == ["OBSERVED"]
    assert grouped["codex-skill-file-access"] == ["OBSERVED"]
    assert grouped["codex-mcp-tool-call"] == ["OBSERVED"]
    assert grouped["codex-file-change"] == ["OBSERVED"]

    malformed = "{not-json}\n" + event("turn.completed")
    observations = parse_codex_jsonl(malformed)
    grouped = results(observations)
    assert grouped["codex-jsonl-event-stream"] == ["OBSERVED"]
    assert grouped["codex-jsonl-parse-warning"] == ["OBSERVED"]

    unknown = event("future.event", answer="do not infer")
    observations = parse_codex_jsonl(unknown)
    grouped = results(observations)
    assert grouped["codex-jsonl-event-stream"] == ["OBSERVED"]
    assert len(observations) == 2, "unknown events should only create the stream and parse-warning observations"
    assert grouped["codex-jsonl-parse-warning"] == ["OBSERVED"]

    top_level_error = event("error", message="stream failure")
    observations = parse_codex_jsonl(top_level_error)
    grouped = results(observations)
    assert grouped["codex-stream-error"] == ["OBSERVED"]
    assert grouped["codex-jsonl-event-stream"] == ["OBSERVED"]

    item_error = event("item.completed", {"type": "error", "message": "recoverable item error"})
    observations = parse_codex_jsonl(item_error)
    grouped = results(observations)
    assert grouped["codex-jsonl-event-stream"] == ["OBSERVED"]
    assert len(observations) == 1, "item-level errors must not be promoted to semantic stream errors"
    assert "codex-stream-error" not in grouped

    malformed_item = event("item.completed")
    observations = parse_codex_jsonl(malformed_item)
    grouped = results(observations)
    assert grouped["codex-jsonl-event-stream"] == ["OBSERVED"]
    assert grouped["codex-jsonl-parse-warning"] == ["OBSERVED"]

    print("Codex JSONL parser edge-case tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
