from core.runtime.v2_1.engine import Agent, AgentContract, Evaluation, Evidence, Role, RuntimeEngine, WorkUnit
import pytest

def _engine():
    r=RuntimeEngine()
    r.register_agent(Agent("reviewer",frozenset({"read","execute"}),frozenset({"read","execute"})))
    r.register_role(Role("reviewer",("review","accept"),frozenset({"read","execute"})))
    r.create_work_unit(WorkUnit("wu-human","human approval boundary","reviewer",("review complete",)))
    r.bind(AgentContract("contract-human","wu-human","reviewer","reviewer",frozenset({"read","execute"}),{}, {},("review complete",),("test-result","human-approval")))
    r.start("wu-human")
    r.record_evidence(Evidence("e-test","wu-human","reviewer","test-result","review-pass","fixture"))
    return r

def test_human_approval_is_explicit_actor_and_evidence():
    r=_engine()
    r.record_evidence(Evidence("e-human","wu-human","human:reviewer-1","human-approval","approved","fixture"))
    r.evaluate(Evaluation("eval-human","wu-human",("review complete",),("e-test","e-human"),"PASS","ACCEPTED","human approved after evidence review","human:reviewer-1","human"))
    assert r.work_units["wu-human"].status=="ACCEPTED"
    assert r.evaluations["eval-human"].actor_type=="human"

def test_human_acceptance_requires_human_approval_evidence():
    r=_engine()
    with pytest.raises(ValueError, match="human-approval"):
        r.evaluate(Evaluation("eval-human","wu-human",("review complete",),("e-test",),"PASS","ACCEPTED","missing approval","human:reviewer-1","human"))

def test_accepted_evaluation_must_be_pass():
    r=_engine()
    with pytest.raises(ValueError, match="only PASS"):
        r.evaluate(Evaluation("eval-partial","wu-human",("review complete",),("e-test",),"PARTIAL","ACCEPTED","partial cannot be accepted","reviewer","agent"))
