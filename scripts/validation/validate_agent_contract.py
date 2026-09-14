#!/usr/bin/env python3
"""Validate the bounded AI Developer Agent Contract and orchestrator policy."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "docs/development/multi-agent/agent-contract.schema.json"
CONTRACT_DOC = ROOT / "docs/development/multi-agent/AGENT-CONTRACT.md"
ORCHESTRATOR_DOC = ROOT / "docs/development/multi-agent/ORCHESTRATOR.md"
ORCHESTRATOR_AGENT = ROOT / ".agents/agents/orchestrator/AGENT.md"

ROLES = {
    "file_picker": {"read": True, "write": False, "execute": False, "web": False, "runtime_observe": False},
    "planner": {"read": True, "write": False, "execute": False, "web": False, "runtime_observe": False},
    "web_researcher": {"read": True, "write": False, "execute": False, "web": True, "runtime_observe": False},
    "editor": {"read": True, "write": True, "execute": False, "web": False, "runtime_observe": False},
    "executor": {"read": True, "write": False, "execute": True, "web": False, "runtime_observe": False},
    "terminal_monitor": {"read": True, "write": False, "execute": False, "web": False, "runtime_observe": True},
    "reviewer": {"read": True, "write": False, "execute": False, "web": False, "runtime_observe": False},
    "browser_agent": {"read": True, "write": False, "execute": False, "web": True, "runtime_observe": True},
    "debugger": {"read": True, "write": True, "execute": False, "web": False, "runtime_observe": False},
    "orchestrator": {"read": True, "write": False, "execute": False, "web": False, "runtime_observe": False},
}

STATES = {
    "READY", "ANALYZING", "PLANNING", "EDITING", "EXECUTING", "VALIDATING",
    "REVIEWING", "REQUEST_CHANGES", "PASS", "BLOCKED", "FAILED",
}
STATUSES = {"PASS", "PASS_WITH_CONCERNS", "REQUEST_CHANGES", "BLOCKED", "FAILED"}
STAGES = {"analysis_planning", "coding_execution", "validation_visualization"}
OPERATIONS = {"read", "write", "execute", "observe", "web"}

TRANSITIONS = {
    "READY": {"ANALYZING", "BLOCKED", "FAILED"},
    "ANALYZING": {"PLANNING", "BLOCKED", "FAILED"},
    "PLANNING": {"EDITING", "EXECUTING", "VALIDATING", "BLOCKED", "FAILED"},
    "EDITING": {"EXECUTING", "REQUEST_CHANGES", "BLOCKED", "FAILED"},
    "EXECUTING": {"VALIDATING", "REVIEWING", "REQUEST_CHANGES", "BLOCKED", "FAILED"},
    "VALIDATING": {"REVIEWING", "REQUEST_CHANGES", "BLOCKED", "FAILED", "PASS"},
    "REVIEWING": {"PASS", "REQUEST_CHANGES", "BLOCKED", "FAILED"},
    "REQUEST_CHANGES": {"PLANNING", "EDITING", "BLOCKED", "FAILED"},
    "PASS": set(),
    "BLOCKED": {"PLANNING"},
    "FAILED": {"PLANNING"},
}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"expected JSON object in {path}")
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_schema(schema: dict) -> None:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "contract schema must use Draft 2020-12")
    required = set(schema.get("required", []))
    expected = {
        "contract_version", "invocation_id", "task_id", "agent", "stage", "state", "attempt",
        "objective", "workspace", "allowed_scope", "permissions", "context", "constraints",
        "required_evidence", "stop_conditions", "result",
    }
    require(expected <= required, "contract schema is missing required envelope fields")
    role_enum = set(schema["properties"]["agent"]["properties"]["role"]["enum"])
    require(role_enum == set(ROLES), "contract role enum does not match orchestrator role ceiling")
    state_enum = set(schema["properties"]["state"]["enum"])
    require(state_enum == STATES, "contract state enum does not match lifecycle states")
    stage_enum = set(schema["properties"]["stage"]["enum"])
    require(stage_enum == STAGES, "contract stage enum is incomplete")


def validate_documents() -> None:
    contract = CONTRACT_DOC.read_text(encoding="utf-8")
    orchestrator = ORCHESTRATOR_DOC.read_text(encoding="utf-8")
    agent = ORCHESTRATOR_AGENT.read_text(encoding="utf-8")
    for marker in ("Only the orchestrator may advance global task state", "allowed_scope", "permissions", "required_evidence", "stop_conditions"):
        require(marker in contract, f"contract document missing enforcement marker: {marker}")
    for marker in ("Dispatch gate", "Acceptance gate", "Permission ceiling", "Global state authority", "Retry discipline"):
        require(marker in orchestrator, f"orchestrator document missing policy section: {marker}")
    require("The Orchestrator is the sole coordinator" in agent, "orchestrator agent surface missing sole-coordinator rule")


def validate_permission_ceiling() -> None:
    for role, ceiling in ROLES.items():
        for capability, allowed in ceiling.items():
            if not allowed:
                continue
            require(capability in {"read", "write", "execute", "web", "runtime_observe"}, f"unknown capability: {capability}")


def validate_transition_table() -> None:
    require(set(TRANSITIONS) == STATES, "transition table must cover every global state")
    require("PASS" not in TRANSITIONS["PASS"], "PASS must be terminal")
    for source, targets in TRANSITIONS.items():
        require(targets <= STATES, f"{source} contains an unknown transition target")


def validate_sample_contract() -> None:
    sample = {
        "contract_version": "1.0",
        "invocation_id": "INV-TEST-001",
        "task_id": "MA-001",
        "agent": {"role": "planner", "version": "1.0"},
        "stage": "analysis_planning",
        "state": "PLANNING",
        "attempt": 1,
        "objective": "validate contract enforcement",
        "workspace": {"repository": "eaglesjo/codingStandard-dev", "ref": "test"},
        "allowed_scope": {"paths": ["docs/development/"], "operations": ["read"]},
        "permissions": ROLES["planner"].copy(),
        "context": {"durable_state_refs": ["CURRENT.md"], "evidence_refs": [], "input_artifact_refs": []},
        "constraints": ["read-only"],
        "required_evidence": ["plan"],
        "stop_conditions": ["scope ambiguity"],
        "result": {"status": "PASS", "findings": [], "changes": [], "evidence": [], "risks": [], "blockers": [], "artifacts": [], "next_action": "editor"},
    }
    require(sample["agent"]["role"] in ROLES, "sample role is invalid")
    require(all(sample["permissions"][k] <= ROLES["planner"][k] for k in sample["permissions"]), "sample exceeds planner permission ceiling")
    require(set(sample["allowed_scope"]["operations"]) <= OPERATIONS, "sample contains undeclared operation")
    require(sample["attempt"] == 1, "initial invocation attempt must be 1")
    require(sample["result"]["status"] in STATUSES, "sample result status is invalid")
    require(bool(sample["required_evidence"]), "sample must declare required evidence")
    require(bool(sample["stop_conditions"]), "sample must declare stop conditions")


def main() -> int:
    validate_schema(load_json(SCHEMA_PATH))
    validate_documents()
    validate_permission_ceiling()
    validate_transition_table()
    validate_sample_contract()
    print("agent contract enforcement validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
