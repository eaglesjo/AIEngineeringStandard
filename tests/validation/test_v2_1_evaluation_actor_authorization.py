from core.runtime.v2_1.engine import Acceptance, Agent, AgentContract, Evaluation, Evidence, Handoff, Role, RuntimeEngine, WorkUnit
import pytest


def _runtime() -> RuntimeEngine:
    runtime = RuntimeEngine()
    for agent_id in ("owner", "reviewer", "outsider"):
        runtime.register_agent(
            Agent(agent_id, frozenset({"read", "execute"}), frozenset({"read", "execute"}))
        )
        runtime.register_role(
            Role(agent_id, ("review",), frozenset({"read", "execute"}))
        )
    runtime.create_work_unit(
        WorkUnit("wu-actor", "evaluate actor authorization", "owner", ("accepted",))
    )
    runtime.bind(
        AgentContract(
            "contract-owner",
            "wu-actor",
            "owner",
            "owner",
            frozenset({"read", "execute"}),
            {},
            {},
            ("accepted",),
            ("test-result",),
        )
    )
    runtime.start("wu-actor")
    runtime.record_evidence(
        Evidence("e-actor", "wu-actor", "owner", "test-result", "pass", "fixture")
    )
    return runtime


def _evaluation(actor_id: str) -> Evaluation:
    return Evaluation(
        "eval-actor",
        "wu-actor",
        ("accepted",),
        ("e-actor",),
        "PASS",
        Acceptance("ACCEPTED", "authorized evaluation"),
        actor_id,
        "agent",
    )


def test_evaluation_actor_must_be_owner_or_handoff_receiver():
    runtime = _runtime()
    with pytest.raises(ValueError, match="not authorized"):
        runtime.evaluate(_evaluation("outsider"))


def test_handoff_receiver_is_authorized_evaluation_actor():
    runtime = _runtime()
    runtime.handoff(
        Handoff(
            "handoff-actor",
            "wu-actor",
            "owner",
            "reviewer",
            "payload-1",
            ("e-actor",),
            "ready for review",
            runtime.timestamp(),
        )
    )
    runtime.evaluate(_evaluation("reviewer"))
    assert runtime.work_units["wu-actor"].status == "ACCEPTED"


def test_work_unit_owner_remains_authorized_without_handoff():
    runtime = _runtime()
    runtime.evaluate(_evaluation("owner"))
    assert runtime.work_units["wu-actor"].status == "ACCEPTED"
