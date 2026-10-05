#!/usr/bin/env python3
"""Validate the canonical AI Engineering Standard 2.1 contract set."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "core" / "contracts" / "2.1"
EXPECTED = ("agent.schema.json","agent-role.schema.json","agent-contract.schema.json","work-unit.schema.json","handoff.schema.json","evidence.schema.json","evaluation.schema.json")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
def fail(message: str) -> None:
    print(f"2.1 contract validation failed: {message}", file=sys.stderr); raise SystemExit(1)
def load(name: str) -> dict:
    path = CONTRACTS / name
    if not path.is_file(): fail(f"missing contract: {name}")
    try: value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc: fail(f"invalid JSON in {name}: {exc}")
    if not isinstance(value, dict): fail(f"{name} must contain an object")
    return value
def validate_schema(name: str, schema: dict) -> None:
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema": fail(f"{name} must use JSON Schema Draft 2020-12")
    if schema.get("properties", {}).get("schema_version", {}).get("const") != "2.1.0": fail(f"{name} must declare schema_version=2.1.0")
    if schema.get("type") != "object": fail(f"{name} root type must be object")
    required = schema.get("required")
    properties = schema.get("properties")
    if not isinstance(required, list) or not required: fail(f"{name} must declare required fields")
    if not isinstance(properties, dict): fail(f"{name} must declare properties")
    for key in required:
        if key not in properties: fail(f"{name} required field has no property definition: {key}")
def main() -> int:
    schemas = {name: load(name) for name in EXPECTED}
    for name, schema in schemas.items(): validate_schema(name, schema)
    sample_ids = ["planner","planner","contract-1","wu-1","handoff-1","evidence-1","eval-1"]
    if any(not ID_RE.fullmatch(value) for value in sample_ids): fail("reference identifier format is invalid")
    evaluation = schemas["evaluation.schema.json"]
    if "allOf" not in evaluation: fail("evaluation contract must define acceptance constraints")
    print("AIEngineeringStandard 2.1 contract validation passed")
    return 0
if __name__ == "__main__": raise SystemExit(main())
