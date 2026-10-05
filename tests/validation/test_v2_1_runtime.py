from core.runtime.v2_1.engine import Agent, AgentContract, Evaluation, Evidence, Handoff, Role, RuntimeEngine, WorkUnit
import pytest

def ready_engine():
    r=RuntimeEngine()
    r.register_agent(Agent("planner",frozenset({"read","execute"}),frozenset({"read","execute"})))
    r.register_role(Role("implementer",("implement","verify"),frozenset({"read","execute"})))
    r.create_work_unit(WorkUnit("wu-1","implement contract","planner",("tests pass",)))
    r.bind(AgentContract("contract-1","wu-1","planner","implementer",frozenset({"read","execute"}),{}, {},("tests pass",),("test-result",)))
    return r

def test_reference_lifecycle_and_acceptance():
    r=ready_engine(); r.start("wu-1")
    r.record_evidence(Evidence("e-1","wu-1","pytest","test-result","tests/validation/test_v2_1_runtime.py","deterministic"))
    r.handoff(Handoff("h-1","wu-1","planner","reviewer","result-1",("e-1",),"review",r.timestamp()))
    r.evaluate(Evaluation("eval-1","wu-1",("tests pass",),("e-1",),"PASS","ACCEPTED","required tests passed"))
    assert r.work_units["wu-1"].status=="ACCEPTED"

def test_permission_ceiling_is_enforced():
    r=RuntimeEngine()
    with pytest.raises(PermissionError): r.register_agent(Agent("unsafe",frozenset({"read"}),frozenset({"read","write"})))

def test_effective_permissions_must_be_intersection():
    r=ready_engine()
    with pytest.raises(PermissionError): r.bind(AgentContract("bad","wu-1","planner","implementer",frozenset({"read"}),{}, {},("tests pass",),("test-result",)))

def test_missing_evidence_blocks_handoff():
    r=ready_engine(); r.start("wu-1")
    with pytest.raises(ValueError): r.handoff(Handoff("h-1","wu-1","planner","reviewer","result",("missing",),"review",r.timestamp()))

def test_failure_preserves_retry_lineage():
    r=ready_engine(); r.start("wu-1")
    r.record_evidence(Evidence("failure-1","wu-1","runtime","log","failure-1","blocked"))
    r.work_units["wu-1"].status="BLOCKED"
    retry=r.retry("wu-1","runtime failure",("failure-1",))
    assert retry.parent_id=="wu-1"
    assert retry.status=="CREATED"
    assert retry.retry_reason=="runtime failure"
    assert retry.failure_evidence_refs==("failure-1",)

def test_retry_rejects_missing_failure_provenance():
    r=ready_engine(); r.start("wu-1"); r.work_units["wu-1"].status="BLOCKED"
    with pytest.raises(ValueError): r.retry("wu-1","runtime failure",("missing",))
