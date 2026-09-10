#!/usr/bin/env python3
"""Validate deterministic 2.0 conformance output against a committed expectation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "tests" / "validation" / "fixtures" / "conformance"


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: expected JSON object in {path}")
    return data


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a conformance result against its deterministic fixture.")
    parser.add_argument("--agent", default="codex")
    parser.add_argument("--result", required=True, help="Generated conformance result JSON")
    parser.add_argument("--fixture", help="Expected fixture JSON; defaults to tests/validation/fixtures/conformance/<agent>-static.expected.json")
    args = parser.parse_args()

    result = load_json(Path(args.result))
    fixture = load_json(Path(args.fixture) if args.fixture else FIXTURE_DIR / f"{args.agent}-static.expected.json")

    if fixture.get("runtime_invocation") is not False:
        fail("deterministic fixture must set runtime_invocation=false")
    if result.get("schema_version") != fixture.get("schema_version"):
        fail("schema_version does not match fixture")
    if result.get("standard_version") != fixture.get("standard_version"):
        fail("standard_version does not match fixture")
    if result.get("agent") != fixture.get("agent"):
        fail("agent does not match fixture")
    if result.get("result") != fixture.get("expected_overall"):
        fail(f"overall result mismatch: expected {fixture.get('expected_overall')}, got {result.get('result')}")

    actual_checks = {item.get("id"): item.get("result") for item in result.get("checks", [])}
    expected_checks = fixture.get("expected_static_checks", {})
    if not isinstance(expected_checks, dict) or not expected_checks:
        fail("fixture expected_static_checks must be a non-empty object")
    if actual_checks != expected_checks:
        missing = sorted(set(expected_checks) - set(actual_checks))
        unexpected = sorted(set(actual_checks) - set(expected_checks))
        changed = sorted(k for k in set(expected_checks) & set(actual_checks) if expected_checks[k] != actual_checks[k])
        details = []
        if missing: details.append(f"missing={missing}")
        if unexpected: details.append(f"unexpected={unexpected}")
        if changed: details.append(f"changed={[(k, expected_checks[k], actual_checks[k]) for k in changed]}")
        fail("static check mismatch: " + "; ".join(details))

    print(f"Conformance fixture validation passed: {args.agent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
