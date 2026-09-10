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
EVIDENCE_SCHEMA = ROOT / "core" / "validation" / "conformance-evidence.schema.json"
RUNTIME_SCENARIOS = [
    ROOT / "tests" / "validation" / "fixtures" / "conformance" / "codex-runtime.scenario.json",
    ROOT / "tests" / "validation" / "fixtures" / "conformance" / "codex-runtime-failure-recovery.scenario.json",
]

STATUS_VALUES = {"PASS", "PARTIAL", "ADAPTER", "UNTESTED", "UNSUPPORTED", "FAIL"}
AGENT_STATUS_VALUES = STATUS_VALUES - {"FAIL"}
CHECK_IDS = {"instruction-discovery", "skill-discovery", "skill-loading", "plugin-capability", "mcp-capability", "permission-check", "task-execution", "validation", "failure-recovery", "evidence-reporting"}
SECURITY_CHECK_IDS = {"provenance", "integrity", "permissions", "secrets", "execution-boundary", "instruction-safety", "mcp-boundary", "plugin-boundary"}
OBSERVATION_SOURCES = {"harness", "adapter", "runtime"}
OBSERVATION_METHODS = {"task-assertion", "harness-integrity", "adapter-trace", "direct-runtime"}
OBSERVATION_LEVELS = {"weak", "moderate", "strong"}


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
    ids = set()
    results = {}
    for index, check in enumerate(data["checks"]):
        require(isinstance(check, dict), f"{label} checks[{index}] must be an object")
        require(check.get("id") in CHECK_IDS, f"{label} checks[{index}] has invalid id")
        require(check.get("id") not in ids, f"{label} contains duplicate check id: {check.get('id')}")
        ids.add(check["id"])
        require(check.get("result") in STATUS_VALUES, f"{label} checks[{index}] has invalid result")
        results[check["id"]] = check["result"]

    missing = CHECK_IDS - ids
    if data["result"] in {"PASS", "PARTIAL"}:
        require(not missing, f"{label} is missing mandatory checks: {sorted(missing)}")

    check_results = set(results.values())
    if data["result"] == "PASS":
        require(ids == CHECK_IDS, f"{label} PASS must contain every mandatory check")
        require(check_results == {"PASS"}, f"{label} PASS requires every check to be PASS")
    elif data["result"] == "PARTIAL":
        require("FAIL" not in check_results, f"{label} PARTIAL cannot contain a FAIL check")
        require(check_results != {"PASS"}, f"{label} PARTIAL requires at least one non-PASS check")
    elif data["result"] == "ADAPTER":
        require("ADAPTER" in check_results or "PASS" in check_results, f"{label} ADAPTER must contain adapter/pass evidence")
    elif data["result"] == "UNTESTED":
        require(check_results <= {"UNTESTED", "UNSUPPORTED"}, f"{label} UNTESTED cannot contain executed PASS/FAIL evidence")


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


def validate_evidence_schema(data: object) -> None:
    require(isinstance(data, dict), "conformance evidence schema must be an object")
    require(data.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "unexpected evidence schema dialect")
    require(data.get("title") == "AIEngineeringStandard 2.0 Runtime Conformance Evidence", "unexpected evidence schema title")
    required = data.get("required", [])
    for key in ("schema_version", "standard_version", "agent", "runtime", "repository", "scenario", "started_at", "finished_at", "result", "observations", "checks"):
        require(key in required, f"evidence schema missing required field: {key}")
    enum = data.get("properties", {}).get("result", {}).get("enum", [])
    require(set(enum) == STATUS_VALUES, "evidence schema result enum is incomplete")
    observation = data.get("properties", {}).get("observations", {}).get("items", {})
    obs_required = observation.get("required", [])
    for key in ("id", "source", "method", "evidence_level", "result", "details"):
        require(key in obs_required, f"evidence schema observation missing required field: {key}")
    require(set(observation.get("properties", {}).get("source", {}).get("enum", [])) == OBSERVATION_SOURCES, "observation source enum is incomplete")
    require(set(observation.get("properties", {}).get("method", {}).get("enum", [])) == OBSERVATION_METHODS, "observation method enum is incomplete")
    require(set(observation.get("properties", {}).get("evidence_level", {}).get("enum", [])) == OBSERVATION_LEVELS, "observation evidence level enum is incomplete")
    protected = data.get("properties", {}).get("protected_files", {})
    require(protected.get("type") == "array", "evidence schema protected_files must be an array")
    all_of = data.get("allOf", [])
    require(isinstance(all_of, list) and all_of, "evidence schema must define result-dependent policy rules")
    pass_rule = next((rule for rule in all_of if rule.get("if", {}).get("properties", {}).get("result", {}).get("const") == "PASS"), None)
    require(pass_rule is not None, "evidence schema must define PASS evidence policy")


def validate_runtime_scenario(data: object, label: str) -> None:
    require(isinstance(data, dict), f"{label} must be an object")
    require(data.get("schema_version") == "2.0.0", f"{label} schema_version must be 2.0.0")
    require(data.get("standard_version") == "2.0", f"{label} standard_version must be 2.0")
    require(data.get("agent") == "codex", f"{label} agent must be codex")
    scenario = data.get("scenario")
    require(isinstance(scenario, dict), f"{label} scenario must be an object")
    for key in ("id", "description", "prompt", "expected_markers", "forbidden_markers", "permission_expectations"):
        require(key in scenario, f"{label} missing: {key}")
    require(isinstance(scenario["expected_markers"], list) and scenario["expected_markers"], f"{label} expected_markers must be non-empty")
    require(isinstance(scenario["forbidden_markers"], list), f"{label} forbidden_markers must be an array")
    require(isinstance(scenario["permission_expectations"], dict), f"{label} permission_expectations must be an object")
    if scenario.get("protected_files"):
        require(isinstance(scenario["protected_files"], list), f"{label} protected_files must be an array")
        require(all(isinstance(item, str) and item for item in scenario["protected_files"]), f"{label} protected_files entries must be non-empty strings")


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
    validate_evidence_schema(load(EVIDENCE_SCHEMA))
    for scenario_path in RUNTIME_SCENARIOS:
        validate_runtime_scenario(load(scenario_path), str(scenario_path.relative_to(ROOT)))
    print("AIEngineeringStandard 2.0 schema validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
