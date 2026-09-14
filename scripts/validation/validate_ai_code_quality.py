#!/usr/bin/env python3
"""Validate the minimal AI-generated-code acceptance contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "core/validation/ai-code-quality.schema.json"

REQUIRED_CHECKS = {"scope", "focused_test", "quality_check", "broader_validation", "review"}
PASS = "PASS"


def fail(message: str) -> None:
    print(f"AI code quality validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_schema() -> dict:
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read contract: {exc}")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("contract must use JSON Schema Draft 2020-12")
    if schema.get("properties", {}).get("schema_version", {}).get("const") != "2.0.0":
        fail("contract schema_version must be 2.0.0")
    return schema


def validate_contract(document: dict) -> None:
    if not isinstance(document, dict):
        fail("contract must be an object")
    if document.get("schema_version") != "2.0.0":
        fail("schema_version must be 2.0.0")
    for field in ("task_id", "candidate", "checks", "acceptance"):
        if field not in document:
            fail(f"missing required field: {field}")
    candidate = document["candidate"]
    if not isinstance(candidate, dict) or not candidate.get("revision") or not isinstance(candidate.get("dirty"), bool):
        fail("candidate must contain revision and boolean dirty state")
    checks = document["checks"]
    if not isinstance(checks, list) or not checks:
        fail("checks must be a non-empty array")
    ids = set()
    for check in checks:
        if not isinstance(check, dict):
            fail("each check must be an object")
        ids.add(check.get("id"))
        if check.get("id") not in REQUIRED_CHECKS:
            fail(f"unsupported check id: {check.get('id')}")
        if check.get("result") not in {"PASS", "FAIL", "NOT_RUN"}:
            fail(f"invalid result for {check.get('id')}")
        if not isinstance(check.get("evidence"), str) or not check["evidence"].strip():
            fail(f"missing evidence for {check.get('id')}")
    missing = REQUIRED_CHECKS - ids
    if missing:
        fail(f"missing required checks: {', '.join(sorted(missing))}")
    acceptance = document["acceptance"]
    if not isinstance(acceptance, dict) or acceptance.get("status") not in {"ACCEPTED", "REJECTED", "INCOMPLETE"}:
        fail("invalid acceptance status")
    if not isinstance(acceptance.get("basis"), str) or not acceptance["basis"].strip():
        fail("acceptance basis is required")
    results = {check["id"]: check["result"] for check in checks}
    all_pass = all(results[check_id] == PASS for check_id in REQUIRED_CHECKS)
    if acceptance["status"] == "ACCEPTED" and not all_pass:
        fail("ACCEPTED requires PASS for every required quality check")
    if acceptance["status"] == "ACCEPTED" and candidate["dirty"]:
        fail("ACCEPTED requires a clean candidate revision")


def main() -> int:
    validate_schema()
    sample = {
        "schema_version": "2.0.0",
        "task_id": "validation-fixture",
        "candidate": {"revision": "fixture-revision", "dirty": False},
        "checks": [
            {"id": check_id, "result": "PASS", "evidence": f"fixture evidence for {check_id}"}
            for check_id in sorted(REQUIRED_CHECKS)
        ],
        "acceptance": {"status": "ACCEPTED", "basis": "all required checks passed on a clean candidate"},
    }
    validate_contract(sample)
    print("AI code quality contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
