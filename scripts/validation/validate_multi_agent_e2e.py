#!/usr/bin/env python3
"""Run bounded contract-driven simulations of representative multi-agent flows.

This is an architecture/E2E simulation, not a live model-agent runtime. It verifies
that the documented orchestrator routing, state transitions, retry discipline, and
permission ceilings compose correctly across representative flows.
"""
from __future__ import annotations

from dataclasses import dataclass

PERMISSION_CEILINGS = {
    "file_picker": {"read"},
    "planner": {"read"},
    "web_researcher": {"read", "web"},
    "editor": {"read", "write"},
    "executor": {"read", "execute"},
    "terminal_monitor": {"read", "runtime_observe"},
    "reviewer": {"read"},
    "browser_agent": {"read", "web", "runtime_observe"},
    "debugger": {"read", "write"},
    "orchestrator": {"read"},
}

TRANSITIONS = {
    "READY": {"ANALYZING", "BLOCKED", "FAILED"},
    "ANALYZING": {"PLANNING", "BLOCKED", "FAILED"},
    "PLANNING": {"EDITING", "EXECUTING", "VALIDATING", "BLOCKED", "FAILED"},
    "EDITING": {"EXECUTING", "BLOCKED", "FAILED"},
    "EXECUTING": {"VALIDATING", "BLOCKED", "FAILED"},
    "VALIDATING": {"REVIEWING", "REQUEST_CHANGES", "BLOCKED", "FAILED"},
    "REVIEWING": {"PASS", "REQUEST_CHANGES", "BLOCKED", "FAILED"},
    "REQUEST_CHANGES": {"PLANNING", "BLOCKED", "FAILED"},
    "PASS": set(),
    "BLOCKED": {"PLANNING"},
    "FAILED": {"PLANNING"},
}


@dataclass
class Invocation:
    role: str
    permissions: set[str]
    attempt: int = 1
    parent_invocation_id: str | None = None


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def transition(state: str, new_state: str) -> str:
    assert_true(new_state in TRANSITIONS[state], f"illegal transition: {state} -> {new_state}")
    return new_state


def dispatch(invocation: Invocation) -> None:
    assert_true(invocation.role in PERMISSION_CEILINGS, f"unknown role: {invocation.role}")
    assert_true(
        invocation.permissions <= PERMISSION_CEILINGS[invocation.role],
        f"permission ceiling exceeded for {invocation.role}",
    )
    if invocation.attempt > 1:
        assert_true(bool(invocation.parent_invocation_id), "retry must identify parent invocation")


def happy_path() -> None:
    state = "READY"
    route = ["orchestrator", "file_picker", "planner", "editor", "executor", "reviewer", "orchestrator"]
    permissions = {
        "orchestrator": {"read"},
        "file_picker": {"read"},
        "planner": {"read"},
        "editor": {"read", "write"},
        "executor": {"read", "execute"},
        "reviewer": {"read"},
    }
    for role in route:
        dispatch(Invocation(role, permissions[role]))
        if role == "file_picker":
            state = transition(state, "ANALYZING")
        elif role == "planner":
            state = transition(state, "PLANNING")
        elif role == "editor":
            state = transition(state, "EDITING")
        elif role == "executor":
            state = transition(state, "EXECUTING")
            state = transition(state, "VALIDATING")
        elif role == "reviewer":
            state = transition(state, "REVIEWING")
        elif role == "orchestrator" and state == "REVIEWING":
            state = transition(state, "PASS")
    assert_true(state == "PASS", "happy path did not reach PASS")


def failure_recovery() -> None:
    state = "READY"
    for new_state in ("ANALYZING", "PLANNING", "EDITING", "EXECUTING", "FAILED"):
        state = transition(state, new_state)
    failed = Invocation("executor", {"read", "execute"})
    dispatch(failed)
    debugger = Invocation("debugger", {"read", "write"}, attempt=2, parent_invocation_id="exec-1")
    dispatch(debugger)
    state = transition(state, "PLANNING")
    state = transition(state, "EDITING")
    state = transition(state, "EXECUTING")
    state = transition(state, "VALIDATING")
    state = transition(state, "REVIEWING")
    state = transition(state, "PASS")
    assert_true(state == "PASS", "failure recovery did not return to PASS")


def optional_routing() -> None:
    # Browser and web research are conditional; neither is required for a
    # non-web documentation change.
    route = ["file_picker", "planner", "editor", "reviewer"]
    assert_true("browser_agent" not in route, "browser agent must be conditional")
    assert_true("web_researcher" not in route, "web researcher must be conditional")
    for role in route:
        dispatch(Invocation(role, PERMISSION_CEILINGS[role]))


def main() -> int:
    happy_path()
    failure_recovery()
    optional_routing()
    print("multi-agent E2E simulation passed: happy path, failure recovery, conditional routing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
