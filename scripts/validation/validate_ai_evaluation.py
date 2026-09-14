#!/usr/bin/env python3
"""Validate deterministic, vendor-neutral AI evaluation evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "core/validation/ai-evaluation.schema.json"


def fail(message: str) -> None:
    print(f"AI evaluation validation failed: {message}", file=sys.stderr)
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


def validate_contract(document: dict) -> float:
    if not isinstance(document, dict):
        fail("contract must be an object")
    if document.get("schema_version") != "2.0.0":
        fail("schema_version must be 2.0.0")
    for field in ("task_id", "evaluation", "cases", "acceptance"):
        if field not in document:
            fail(f"missing required field: {field}")
    evaluation = document["evaluation"]
    if evaluation != {"method": "deterministic", "deterministic": True}:
        fail("evaluation must declare the deterministic method")
    cases = document["cases"]
    if not isinstance(cases, list) or not cases:
        fail("cases must be a non-empty array")
    seen_ids = set()
    scores = []
    for case in cases:
        if not isinstance(case, dict):
            fail("each case must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip() or case_id in seen_ids:
            fail("case ids must be unique, non-empty strings")
        seen_ids.add(case_id)
        if not isinstance(case.get("input"), str) or not case["input"].strip():
            fail(f"input is required for {case_id}")
        criteria = case.get("expected_criteria")
        if not isinstance(criteria, list) or not criteria:
            fail(f"expected_criteria must be non-empty for {case_id}")
        results = []
        criterion_ids = set()
        for criterion in criteria:
            if not isinstance(criterion, dict):
                fail(f"criterion must be an object for {case_id}")
            criterion_id = criterion.get("id")
            if not isinstance(criterion_id, str) or not criterion_id.strip() or criterion_id in criterion_ids:
                fail(f"criterion ids must be unique within {case_id}")
            criterion_ids.add(criterion_id)
            if criterion.get("result") not in {"PASS", "FAIL"}:
                fail(f"invalid criterion result for {case_id}/{criterion_id}")
            if not isinstance(criterion.get("evidence"), str) or not criterion["evidence"].strip():
                fail(f"missing criterion evidence for {case_id}/{criterion_id}")
            results.append(criterion["result"])
        calculated = results.count("PASS") / len(results)
        if abs(case["score"] - calculated) > 1e-9:
            fail(f"score mismatch for {case_id}: expected {calculated:.6f}, got {case['score']:.6f}")
        if not isinstance(case.get("evidence"), str) or not case["evidence"].strip():
            fail(f"missing case evidence for {case_id}")
        scores.append(calculated)
    acceptance = document["acceptance"]
    if not isinstance(acceptance, dict):
        fail("acceptance must be an object")
    status = acceptance.get("status")
    threshold = acceptance.get("threshold")
    if status not in {"ACCEPTED", "REJECTED", "INCOMPLETE"}:
        fail("invalid acceptance status")
    if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
        fail("acceptance threshold must be between 0 and 1")
    if not isinstance(acceptance.get("basis"), str) or not acceptance["basis"].strip():
        fail("acceptance basis is required")
    overall = sum(scores) / len(scores)
    if status == "ACCEPTED" and overall < threshold:
        fail(f"ACCEPTED requires overall score >= threshold ({overall:.6f} < {threshold:.6f})")
    return overall


def main() -> int:
    validate_schema()
    sample = {
        "schema_version": "2.0.0",
        "task_id": "validation-fixture",
        "evaluation": {"method": "deterministic", "deterministic": True},
        "cases": [
            {
                "id": "case-1",
                "input": "fixture input",
                "expected_criteria": [
                    {"id": "criterion-1", "result": "PASS", "evidence": "criterion observed"},
                    {"id": "criterion-2", "result": "PASS", "evidence": "criterion observed"}
                ],
                "score": 1.0,
                "evidence": "case evaluated deterministically"
            }
        ],
        "acceptance": {"status": "ACCEPTED", "threshold": 1.0, "basis": "overall score meets threshold"}
    }
    score = validate_contract(sample)
    print(f"AI evaluation contract validation passed: overall={score:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
