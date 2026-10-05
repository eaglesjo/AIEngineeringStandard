from core.runtime.v2_1.engine import Acceptance, Agent, AgentContract, Evaluation, Evidence, Handoff, Role, RuntimeEngine, WorkUnit
import pytest


def _engine():
    runtime = RuntimeEngine()
    runtime.register_agent(Agent("planner", frozenset({"read", "execute"}), frozenset({"read", "execute"})))
    runtime.register_agent(Agent("reviewer", frozenset({"read", "execute"}), frozenset({"read", "execute"})))
    runtime.register_role(Role("planner", ("plan",), frozenset({"read", "execute"})))
    runtime.create_work_unit(WorkUnit("wu-1", "lifecycle", "planner", ("complete",)))
    runtime.bind(AgentContract(
        "contract-1", "wu-1", "planner", "planner",
        frozenset({"read", "execute"}), {}, {}, ("complete",), ("test-result",)
    ))
    return runtime


def _evidence(runtime):
    runtime.record_evidence(Evidence(
        "e-1", "wu-1", "planner", "test-result", "pass", "fixture"
    ))


def test_handoff_requires_executing_work_unit():
    runtime = _engine()
    with pytest.raises(RuntimeError, match="EXECUTING"):
        runtime.handoff(Handoff(
            "h-1", "wu-1", "planner", "reviewer", "payload", ("e-1",),
            "review", runtime.timestamp()
        ))


def test_evaluation_requires_active_work_unit():
    runtime = _engine()
    _evidence(runtime)
    with pytest.raises(RuntimeError, match="EXECUTING or HANDOFF_PENDING"):
        runtime.evaluate(Evaluation(
            "eval-1", "wu-1", ("complete",), ("e-1",), "PASS", Acceptance("ACCEPTED", "not started"), "planner", "agent"
        ))


def test_incomplete_evaluation_blocks_work_unit():
    runtime = _engine()
    runtime.start("wu-1")
    _evidence(runtime)
    runtime.evaluate(Evaluation(
        "eval-1", "wu-1", ("complete",), ("e-1",), "PARTIAL", Acceptance("INCOMPLETE", "partial evidence"), "planner", "agent"
    ))
    assert runtime.work_units["wu-1"].status == "BLOCKED"


def test_evaluation_rejects_cross_work_unit_evidence():
    runtime = _engine()
    runtime.create_work_unit(WorkUnit("wu-2", "other", "planner", ("other",)))
    runtime.record_evidence(Evidence(
        "e-2", "wu-2", "planner", "test-result", "other-pass", "fixture"
    ))
    runtime.start("wu-1")
    with pytest.raises(ValueError, match="belong to the work unit"):
        runtime.evaluate(Evaluation(
            "eval-1", "wu-1", ("complete",), ("e-2",), "PASS", Acceptance("ACCEPTED", "wrong provenance"), "planner", "agent"
        ))


def test_completed_work_unit_cannot_be_evaluated_twice():
    runtime = _engine()
    runtime.start("wu-1")
    _evidence(runtime)
    runtime.evaluate(Evaluation(
        "eval-1", "wu-1", ("complete",), ("e-1",), "PASS", Acceptance("ACCEPTED", "complete"), "planner", "agent"
    ))
    with pytest.raises(RuntimeError, match="EXECUTING or HANDOFF_PENDING"):
        runtime.evaluate(Evaluation(
            "eval-2", "wu-1", ("complete",), ("e-1",), "PASS", Acceptance("ACCEPTED", "duplicate"), "planner", "agent"
        ))
