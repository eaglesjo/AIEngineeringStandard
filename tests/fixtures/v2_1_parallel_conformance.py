"""Canonical v2.1 parallel work and join conformance fixture."""
from core.runtime.v2_1.engine import Acceptance, Agent, AgentContract, Evidence, Evaluation, Role, RuntimeEngine, WorkUnit

def _bind_and_start(runtime, work_unit, agent_id, contract_id):
    runtime.bind(AgentContract(contract_id, work_unit.id, agent_id, agent_id, frozenset({"read", "execute"}), {}, {}, work_unit.acceptance_criteria, ("test-result",)))
    runtime.start(work_unit.id)

def run() -> dict[str, object]:
    runtime = RuntimeEngine()
    for agent_id in ("implementer-a", "implementer-b", "planner"):
        runtime.register_agent(Agent(agent_id, frozenset({"read", "execute"}), frozenset({"read", "execute"})))
        runtime.register_role(Role(agent_id, ("parallel implementation",), frozenset({"read", "execute"})))

    root = WorkUnit("wu-parallel-root", "complete parallel work", "planner", ("both branches accepted",))
    branch_a = WorkUnit("wu-parallel-a", "complete branch A", "implementer-a", ("branch A passes",), parent_id=root.id)
    branch_b = WorkUnit("wu-parallel-b", "complete branch B", "implementer-b", ("branch B passes",), parent_id=root.id)
    for work_unit in (root, branch_a, branch_b):
        runtime.create_work_unit(work_unit)

    _bind_and_start(runtime, branch_a, "implementer-a", "contract-parallel-a")
    _bind_and_start(runtime, branch_b, "implementer-b", "contract-parallel-b")
    runtime.record_evidence(Evidence("e-parallel-a", branch_a.id, "implementer-a", "test-result", "branch-a-pass", "fixture"))
    runtime.record_evidence(Evidence("e-parallel-b", branch_b.id, "implementer-b", "test-result", "branch-b-pass", "fixture"))
    runtime.evaluate(Evaluation("eval-parallel-a", branch_a.id, branch_a.acceptance_criteria, ("e-parallel-a",), "PASS", Acceptance("ACCEPTED", "branch A evidence"),"implementer-a","agent"))
    runtime.evaluate(Evaluation("eval-parallel-b", branch_b.id, branch_b.acceptance_criteria, ("e-parallel-b",), "PASS", Acceptance("ACCEPTED", "branch B evidence"),"implementer-b","agent"))

    runtime.bind(AgentContract("contract-parallel-root", root.id, "planner", "planner", frozenset({"read", "execute"}), {}, {}, root.acceptance_criteria, ("test-result",)))
    runtime.start(root.id)
    runtime.record_evidence(Evidence("e-parallel-join", root.id, "planner", "test-result", "both-branches-accepted", "fixture"))
    runtime.evaluate(Evaluation("eval-parallel-root", root.id, root.acceptance_criteria, ("e-parallel-join",), "PASS", Acceptance("ACCEPTED", "explicit join evidence after both child evaluations"), "planner", "agent"))

    return {"work_units": {root.id: root.status, branch_a.id: branch_a.status, branch_b.id: branch_b.status}, "parents": {branch_a.id: branch_a.parent_id, branch_b.id: branch_b.parent_id}, "evaluations": sorted(runtime.evaluations), "join_evidence": ["e-parallel-join"]}
