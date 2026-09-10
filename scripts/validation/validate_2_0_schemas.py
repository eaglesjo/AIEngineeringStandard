#!/usr/bin/env python3
"""Validate AIEngineeringStandard 2.0 machine-readable foundation contracts."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "compatibility" / "agents.json"
RESULT_SCHEMA = ROOT / "core" / "validation" / "conformance-result.schema.json"
FIXTURE = ROOT / "tests" / "validation" / "fixtures" / "conformance-result.pass.json"
SECURITY_SCHEMA = ROOT / "core" / "validation" / "security-result.schema.json"
SECURITY_FIXTURE = ROOT / "tests" / "validation" / "fixtures" / "security-result.pass.json"

STATUS_VALUES = {"PASS", "PARTIAL", "ADAPTER", "UNTESTED", "UNSUPPORTED", "FAIL"}
AGENT_STATUS_VALUES = STATUS_VALUES - {"FAIL"}
CHECK_IDS = {"instruction-discovery", "skill-discovery", "skill-loading", "plugin-capability", "mcp-capability", "permission-check", "task-execution", "validation", "failure-recovery", "evidence-reporting"}
SECURITY_CHECK_IDS = {"provenance", "integrity", "permissions", "secrets", "execution-boundary", "instruction-safety", "mcp-boundary", "plugin-boundary"}


def load(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON in {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ERROR: {message}")


def validate_agents(data: object) -> None:
    require(isinstance(data, dict), "compatibility/agents.json must be an object")
    require(data.get("schema_version") == "2.0.0", "agents schema_version must be 2.0.0")
    require(data.get("standard_version") == "2.0", "agents standard_version must be 2.0")
    agents = data.get("agents")
    require(isinstance(agents, list), "agents must be an array")
    for index, agent in enumerate(agents):
        require(isinstance(agent, dict), f"agents[{index}] must be an object")
        for key in ("id", "name", "tier", "status", "capabilities"):
            require(key in agent, f"agents[{index}] missing required field: {key}")
        require(bool(re.fullmatch(r"[a-z0-9][a-z0-9._-]*", agent["id"])), f"invalid agent id: {agent['id']!r}")
        require(agent["tier"] in {"P0", "P1", "P2"}, f"invalid tier for {agent['id']}: {agent['tier']}")
        require(agent["status"] in AGENT_STATUS_VALUES, f"invalid status for {agent['id']}: {agent['status']}")
        require(isinstance(agent["capabilities"], dict), f"capabilities must be an object for {agent['id']}")
        for capability, status in agent["capabilities"].items():
            require(status in AGENT_STATUS_VALUES, f"invalid capability status {status!r} for {agent['id']}:{capability}")


def validate_result(data: object, label: str) -> None:
    require(isinstance(data, dict), f"{label} must be an object")
    for key in ("schema_version", "standard_version", "agent", "tested_at", "result", "checks"):
        require(key in data, f"{label} missing required field: {key}")
    require(data["schema_version"] == "2.0.0", f"{label} schema_version must be 2.0.0")
    require(bool(re.fullmatch(r"2\.[0-9]+", data["standard_version"])), f"{label} has invalid standard_version")
    require(isinstance(data["agent"], str) and data["agent"], f"{label} agent must be non-empty")
    require(isinstance(data["tested_at"], str) and data["tested_at"].endswith("Z"), f"{label} tested_at must be UTC ISO-8601")
    require(data["result"] in STATUS_VALUES, f"{label} has invalid result")
    require(isinstance(data["checks"], list) and data["checks"], f"{label} checks must be a non-empty array")
    for index, check in enumerate(data["checks"]):
        require(isinstance(check, dict), f"{label} checks[{index}] must be an object")
        require(check.get("id") in CHECK_IDS, f"{label} checks[{index}] has invalid id")
        require(check.get("result") in STATUS_VALUES, f"{label} checks[{index}] has invalid result")


def validate_security_result(data: object) -> None:
    require(isinstance(data, dict), "security fixture must be an object")
    for key in ("schema_version", "standard_version", "component", "trust", "checks"):
        require(key in data, f"security fixture missing required field: {key}")
    require(data["schema_version"] == "2.0.0", "security fixture schema_version must be 2.0.0")
    require(bool(re.fullmatch(r"2\.[0-9]+", data["standard_version"])), "security fixture has invalid standard_version")
    require(data["trust"] in {"UNTRUSTED", "REVIEWED", "VERIFIED"}, "security fixture has invalid trust")
    require(isinstance(data["checks"], list) and data["checks"], "security fixture checks must be non-empty")
    for index, check in enumerate(data["checks"]):
        require(isinstance(check, dict), f"security fixture checks[{index}] must be an object")
        require(check.get("id") in SECURITY_CHECK_IDS, f"security fixture checks[{index}] has invalid id")
        require(check.get("result") in {"PASS", "FAIL", "UNTESTED"}, f"security fixture checks[{index}] has invalid result")
    if data["trust"] == "VERIFIED":
        require(data.get("version_or_commit"), "VERIFIED security result requires version_or_commit")


def main() -> int:
    validate_agents(load(AGENTS))
    schema = load(RESULT_SCHEMA)
    require(isinstance(schema, dict), "conformance result schema must be an object")
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "unexpected JSON Schema dialect")
    require(schema.get("title") == "AIEngineeringStandard 2.0 Conformance Result", "unexpected conformance schema title")
    validate_result(load(FIXTURE), "conformance fixture")
    security_schema = load(SECURITY_SCHEMA)
    require(isinstance(security_schema, dict), "security result schema must be an object")
    require(security_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "unexpected security schema dialect")
    validate_security_result(load(SECURITY_FIXTURE))
    print("AIEngineeringStandard 2.0 schema validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
