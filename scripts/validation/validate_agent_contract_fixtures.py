#!/usr/bin/env python3
"""Validate representative bounded multi-agent contract fixtures."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/validation/fixtures/multi-agent"
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
OPS = {"read": "read", "write": "write", "execute": "execute", "web": "web", "observe": "runtime_observe"}
REQUIRED = {"contract_version", "invocation_id", "task_id", "agent", "stage", "state", "attempt", "objective", "workspace", "allowed_scope", "permissions", "context", "constraints", "required_evidence", "stop_conditions", "result"}
STATUSES = {"PASS", "PASS_WITH_CONCERNS", "REQUEST_CHANGES", "BLOCKED", "FAILED"}


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(name: str) -> dict:
    with (FIXTURES / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate(contract: dict) -> None:
    assert_true(REQUIRED <= set(contract), "missing required envelope field")
    role = contract["agent"]["role"]
    assert_true(role in ROLES, f"unknown role: {role}")
    permissions = contract["permissions"]
    assert_true(set(permissions) == set(ROLES[role]), "incomplete permission set")
    assert_true(all(not value or ROLES[role][key] for key, value in permissions.items()), "permission ceiling exceeded")
    for operation in contract["allowed_scope"]["operations"]:
        assert_true(operation in OPS, f"unknown operation: {operation}")
        assert_true(permissions[OPS[operation]], f"scope operation {operation} is not authorized")
    assert_true(contract["result"]["status"] in STATUSES, "invalid result status")
    assert_true(contract["required_evidence"], "required evidence missing")
    assert_true(contract["stop_conditions"], "stop conditions missing")
    if contract["attempt"] > 1:
        assert_true(bool(contract.get("parent_invocation_id")), "retry must identify parent invocation")


def main() -> int:
    valid = load("valid-sequential-flow.json")
    validate(valid)
    assert_true(valid["agent"]["role"] == "orchestrator", "valid fixture must represent orchestrator acceptance")
    assert_true("File Picker -> Planner -> Editor -> Executor -> Reviewer -> Orchestrator -> PASS" in valid["result"]["evidence"][0]["value"], "representative flow is incomplete")

    recovery = load("failure-recovery.json")
    validate(recovery)
    assert_true(recovery["attempt"] == 2, "recovery fixture must exercise attempt 2")
    assert_true(recovery["result"]["next_action"] == "executor", "debugger must hand execution to Executor")

    invalid = load("invalid-permission-scope.json")
    try:
        validate(invalid)
    except AssertionError:
        pass
    else:
        raise AssertionError("invalid permission/scope fixture was unexpectedly accepted")

    print("multi-agent contract fixtures passed: valid flow, permission rejection, failure recovery")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
