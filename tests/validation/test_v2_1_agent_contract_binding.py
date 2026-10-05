from core.runtime.v2_1.engine import Agent, AgentContract, Role, RuntimeEngine, WorkUnit
import pytest


def _runtime() -> RuntimeEngine:
    runtime = RuntimeEngine()
    runtime.register_agent(
        Agent("planner", frozenset({"read", "execute"}), frozenset({"read", "execute"}))
    )
    runtime.register_agent(
        Agent("reviewer", frozenset({"read"}), frozenset({"read"}))
    )
    runtime.register_role(
        Role("implementer", ("implement",), frozenset({"read", "execute"}))
    )
    runtime.create_work_unit(
        WorkUnit("wu-1", "implement", "planner", ("tests pass",))
    )
    return runtime


def _contract(contract_id: str, work_unit_id: str = "wu-1", agent_id: str = "planner") -> AgentContract:
    return AgentContract(
        contract_id,
        work_unit_id,
        agent_id,
        "implementer",
        frozenset({"read", "execute"}),
        {},
        {},
        ("tests pass",),
        ("test-result",),
    )


def test_contract_agent_must_own_work_unit():
    runtime = _runtime()
    with pytest.raises(ValueError, match="agent must own the work unit"):
        runtime.bind(_contract("contract-reviewer", agent_id="reviewer"))


def test_work_unit_can_have_only_one_agent_contract():
    runtime = _runtime()
    runtime.bind(_contract("contract-1"))
    with pytest.raises(ValueError, match="already has an agent contract"):
        runtime.bind(_contract("contract-2"))


def test_valid_owner_contract_binds_once():
    runtime = _runtime()
    runtime.bind(_contract("contract-1"))
    assert runtime.contracts["contract-1"].agent_id == "planner"
    assert runtime.work_units["wu-1"].status == "READY"
