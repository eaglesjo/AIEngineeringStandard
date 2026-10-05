from core.runtime.v2_1.engine import Agent, AgentContract, Evidence, Handoff, Role, RuntimeEngine, WorkUnit
import pytest


def test_agent_identity_cannot_be_overwritten():
    runtime = RuntimeEngine()
    runtime.register_agent(Agent("planner", frozenset({"read"}), frozenset({"read"})))
    with pytest.raises(ValueError, match="agent already exists"):
        runtime.register_agent(Agent("planner", frozenset({"read", "execute"}), frozenset({"read"})))
    assert runtime.agents["planner"].capabilities == frozenset({"read"})


def test_role_identity_cannot_be_overwritten():
    runtime = RuntimeEngine()
    runtime.register_role(Role("planner", ("plan",), frozenset({"read"})))
    with pytest.raises(ValueError, match="role already exists"):
        runtime.register_role(Role("planner", ("replace",), frozenset({"execute"})))
    assert runtime.roles["planner"].responsibilities == ("plan",)


def test_agent_contract_identity_cannot_cross_work_units():
    runtime = RuntimeEngine()
    runtime.register_agent(Agent("planner", frozenset({"read"}), frozenset({"read"})))
    runtime.register_role(Role("planner", ("plan",), frozenset({"read"})))
    runtime.create_work_unit(WorkUnit("wu-1", "first", "planner", ("done",)))
    runtime.create_work_unit(WorkUnit("wu-2", "second", "planner", ("done",)))
    runtime.bind(AgentContract(
        "contract-1", "wu-1", "planner", "planner",
        frozenset({"read"}), {}, {}, ("done",), ("test-result",)
    ))
    with pytest.raises(ValueError, match="agent contract already exists"):
        runtime.bind(AgentContract(
            "contract-1", "wu-2", "planner", "planner",
            frozenset({"read"}), {}, {}, ("done",), ("test-result",)
        ))
    assert runtime.contracts["contract-1"].work_unit_id == "wu-1"


def test_handoff_identity_cannot_cross_work_units():
    runtime = RuntimeEngine()
    runtime.register_agent(Agent("sender", frozenset({"read"}), frozenset({"read"})))
    runtime.register_agent(Agent("receiver", frozenset({"read"}), frozenset({"read"})))
    runtime.register_role(Role("sender", ("transfer",), frozenset({"read"})))
    runtime.create_work_unit(WorkUnit("wu-1", "first", "sender", ("done",)))
    runtime.create_work_unit(WorkUnit("wu-2", "second", "sender", ("done",)))
    for work_unit_id, contract_id, evidence_id in (
        ("wu-1", "contract-1", "e-1"),
        ("wu-2", "contract-2", "e-2"),
    ):
        runtime.bind(AgentContract(
            contract_id, work_unit_id, "sender", "sender",
            frozenset({"read"}), {}, {}, ("done",), ("test-result",)
        ))
        runtime.start(work_unit_id)
        runtime.record_evidence(Evidence(
            evidence_id, work_unit_id, "sender", "test-result", "pass", "fixture"
        ))
    runtime.handoff(Handoff(
        "handoff-1", "wu-1", "sender", "receiver", "payload-1", ("e-1",),
        "first transfer", runtime.timestamp()
    ))
    with pytest.raises(ValueError, match="handoff already exists"):
        runtime.handoff(Handoff(
            "handoff-1", "wu-2", "sender", "receiver", "payload-2", ("e-2",),
            "second transfer", runtime.timestamp()
        ))
    assert runtime.handoffs["handoff-1"].work_unit_id == "wu-1"
