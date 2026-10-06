from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "core" / "runtime" / "execution" / "mission.schema.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> int:
    if not SCHEMA.is_file():
        fail(f"missing execution mission schema: {SCHEMA}")
    try:
        document = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid execution mission schema JSON: {exc}")
    if document.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("execution mission schema must use JSON Schema Draft 2020-12")
    if document.get("properties", {}).get("schema_version", {}).get("const") != "1.0.0":
        fail("execution mission schema version must be 1.0.0")
    if document.get("type") != "object" or document.get("additionalProperties") is not False:
        fail("execution mission schema must be a closed object")
    required = {"schema_version", "id", "repository", "source_sha", "purpose", "inputs", "operations", "expected_outputs", "permissions", "terminal_state", "verification", "capability_inventory", "lifecycle", "remote_state"}
    if set(document.get("required", [])) != required:
        fail("execution mission required fields do not match the canonical set")
    permissions = document["properties"]["permissions"]
    if permissions.get("additionalProperties") is not False:
        fail("execution mission permissions must be closed")
    verification = document["properties"]["verification"]
    if verification.get("properties", {}).get("source_sha", {}).get("const") is not True:
        fail("execution mission must require source SHA verification")
    if verification.get("properties", {}).get("outputs", {}).get("minItems") != 1:
        fail("execution mission must require output verification")
    if not SHA_RE.fullmatch("0" * 40):
        fail("execution mission source SHA format is invalid")
    print("AIEngineeringStandard execution mission validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
