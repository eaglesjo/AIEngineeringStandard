"""Canonical v2.1 multi-agent conformance fixture."""
from core.runtime.v2_1.engine import Agent, AgentContract, Evaluation, Evidence, Handoff, Role, RuntimeEngine, WorkUnit

def run() -> dict[str, object]:
    r = RuntimeEngine()
    r.register_agent(Agent("planner", frozenset({"read", "execute"}), frozenset({"read", "execute"})))
    r.register_agent(Agent("implementer", frozenset({"read", "write", "execute"}), frozenset({"read", "write", "execute"})))
    r.register_agent(Agent("verifier", frozenset({"read", "execute"}), frozenset({"read", "execute"})))
    for role in (
        Role("planner", ("decompose",), frozenset({"read", "execute"})),
        Role("implementer", ("implement",), frozenset({"read", "write", "execute"})),
        Role("verifier", ("verify",), frozenset({"read", "execute"})),
    ): r.register_role(role)
    root = WorkUnit("wu-root", "deliver verified artifact", "planner", ("artifact verified",))
    child = WorkUnit("wu-implementation", "implement artifact", "implementer", ("implementation evidence exists",), parent_id=root.id)
    verify = WorkUnit("wu-verification", "verify artifact", "verifier", ("verification passes",), parent_id=root.id)
    for wu in (root, child, verify): r.create_work_unit(wu)
    r.bind(AgentContract("contract-planner","wu-root","planner","planner",frozenset({"read","execute"}),{}, {},("artifact verified",),("handoff",)))
    r.bind(AgentContract("contract-implementer","wu-implementation","implementer","implementer",frozenset({"read","write","execute"}),{}, {},("implementation evidence exists",),("artifact","test-result")))
    r.bind(AgentContract("contract-verifier","wu-verification","verifier","verifier",frozenset({"read","execute"}),{}, {},("verification passes",),("test-result",)))
    r.start("wu-root"); r.start("wu-implementation")
    r.record_evidence(Evidence("e-implementation","wu-implementation","implementer","artifact","artifact-1","fixture"))
    r.record_evidence(Evidence("e-tests","wu-implementation","implementer","test-result","tests-1","fixture"))
    r.handoff(Handoff("h-implementation","wu-implementation","implementer","verifier","artifact-1",("e-implementation","e-tests"),"verification",r.timestamp()))
    r.start("wu-verification")
    r.record_evidence(Evidence("e-verification","wu-verification","verifier","test-result","verification-1","fixture"))
    r.handoff(Handoff("h-verification","wu-verification","verifier","planner","verification-1",("e-verification",),"acceptance",r.timestamp()))
    r.evaluate(Evaluation("eval-verification","wu-verification",("verification passes",),("e-verification",),"PASS","ACCEPTED","verified evidence","verifier","agent"))
    r.record_evidence(Evidence("e-root","wu-root","planner","observation","verified-artifact","fixture"))
    r.evaluate(Evaluation("eval-root","wu-root",("artifact verified",),("e-root",),"PASS","ACCEPTED","child verification accepted","planner","agent"))
    return {"work_units": {k:v.status for k,v in r.work_units.items()}, "evidence": sorted(r.evidence), "handoffs": sorted(r.handoffs), "evaluations": sorted(r.evaluations)}
