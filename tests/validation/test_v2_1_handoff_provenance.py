from core.runtime.v2_1.engine import Agent, AgentContract, Evidence, Handoff, Role, RuntimeEngine, WorkUnit
import pytest

def _engine():
    r=RuntimeEngine()
    r.register_agent(Agent("sender",frozenset({"read","execute"}),frozenset({"read","execute"})))
    r.register_agent(Agent("receiver",frozenset({"read","execute"}),frozenset({"read","execute"})))
    r.register_agent(Agent("other",frozenset({"read","execute"}),frozenset({"read","execute"})))
    r.register_role(Role("sender",("implement",),frozenset({"read","execute"})))
    r.create_work_unit(WorkUnit("wu-handoff","transfer verified work","sender",("handoff complete",)))
    r.bind(AgentContract("contract-sender","wu-handoff","sender","sender",frozenset({"read","execute"}),{}, {},("handoff complete",),("test-result",)))
    r.start("wu-handoff")
    r.record_evidence(Evidence("e-handoff","wu-handoff","sender","test-result","verified-output","fixture"))
    return r

def _handoff(**kwargs):
    values=dict(id="h-1",work_unit_id="wu-handoff",sender="sender",receiver="receiver",payload_ref="artifact-1",evidence_refs=("e-handoff",),reason="ready for verification",timestamp="2026-10-05T00:00:00+00:00")
    values.update(kwargs)
    return Handoff(**values)

def test_handoff_requires_authorized_owner_and_registered_receiver():
    r=_engine()
    r.handoff(_handoff())
    assert r.work_units["wu-handoff"].status=="HANDOFF_PENDING"

def test_handoff_rejects_non_owner_sender():
    r=_engine()
    with pytest.raises(ValueError, match="must own"):
        r.handoff(_handoff(sender="other"))

def test_handoff_rejects_unknown_receiver():
    r=_engine()
    with pytest.raises(ValueError, match="receiver agent"):
        r.handoff(_handoff(receiver="missing"))

def test_handoff_rejects_evidence_from_another_work_unit():
    r=_engine()
    r.create_work_unit(WorkUnit("wu-other","unrelated","other",("done",)))
    r.record_evidence(Evidence("e-other","wu-other","other","test-result","other-output","fixture"))
    with pytest.raises(ValueError, match="belong to the work unit"):
        r.handoff(_handoff(evidence_refs=("e-other",)))

def test_handoff_requires_reason_and_payload():
    r=_engine()
    with pytest.raises(ValueError, match="reason"):
        r.handoff(_handoff(reason=""))
    with pytest.raises(ValueError, match="payload"):
        r.handoff(_handoff(payload_ref=""))
