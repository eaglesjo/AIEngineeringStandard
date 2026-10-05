"""Canonical v2.1 handoff ownership and provenance conformance fixture."""
from core.runtime.v2_1.engine import Agent, AgentContract, Evidence, Handoff, Role, RuntimeEngine, WorkUnit

def run() -> dict[str, object]:
    runtime = RuntimeEngine()
    runtime.register_agent(Agent("sender", frozenset({"read", "execute"}), frozenset({"read", "execute"})))
    runtime.register_agent(Agent("receiver", frozenset({"read", "execute"}), frozenset({"read", "execute"})))
    runtime.register_role(Role("sender", ("implement",), frozenset({"read", "execute"})))
    work_unit = WorkUnit("wu-handoff", "transfer verified work", "sender", ("handoff complete",))
    runtime.create_work_unit(work_unit)
    runtime.bind(AgentContract("contract-sender", work_unit.id, "sender", "sender", frozenset({"read", "execute"}), {}, {}, work_unit.acceptance_criteria, ("test-result",)))
    runtime.start(work_unit.id)
    runtime.record_evidence(Evidence("e-handoff", work_unit.id, "sender", "test-result", "verified-output", "fixture"))
    runtime.handoff(Handoff("h-handoff", work_unit.id, "sender", "receiver", "artifact-1", ("e-handoff",), "ready for verification", "2026-10-05T00:00:00+00:00"))
    return {"status": work_unit.status, "sender": "sender", "receiver": "receiver", "evidence": ["e-handoff"], "payload_ref": "artifact-1"}
