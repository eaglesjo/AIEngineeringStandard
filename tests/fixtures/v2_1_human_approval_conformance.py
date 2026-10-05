"""Canonical v2.1 human approval and intervention conformance fixture."""
from core.runtime.v2_1.engine import Agent, AgentContract, Evaluation, Evidence, Role, RuntimeEngine, WorkUnit

def run() -> dict[str, object]:
    runtime = RuntimeEngine()
    runtime.register_agent(Agent("reviewer", frozenset({"read", "execute"}), frozenset({"read", "execute"})))
    runtime.register_role(Role("reviewer", ("review", "accept"), frozenset({"read", "execute"})))
    work_unit = WorkUnit("wu-human-approval", "approve reviewed work", "reviewer", ("review complete",))
    runtime.create_work_unit(work_unit)
    runtime.bind(AgentContract("contract-human-approval", work_unit.id, "reviewer", "reviewer", frozenset({"read", "execute"}), {}, {}, work_unit.acceptance_criteria, ("test-result", "human-approval")))
    runtime.start(work_unit.id)
    runtime.record_evidence(Evidence("e-human-test", work_unit.id, "reviewer", "test-result", "review-pass", "fixture"))
    runtime.record_evidence(Evidence("e-human-approval", work_unit.id, "human:reviewer-1", "human-approval", "approved", "fixture"))
    runtime.evaluate(Evaluation("eval-human-approval", work_unit.id, work_unit.acceptance_criteria, ("e-human-test", "e-human-approval"), "PASS", "ACCEPTED", "human approval after evidence review", "human:reviewer-1", "human"))
    return {"status": work_unit.status, "actor": runtime.evaluations["eval-human-approval"].actor_id, "actor_type": runtime.evaluations["eval-human-approval"].actor_type, "approval_evidence": ["e-human-approval"]}
