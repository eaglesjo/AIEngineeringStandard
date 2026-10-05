"""Canonical v2.1 retry and recovery conformance fixture."""
from core.runtime.v2_1.engine import Agent, AgentContract, Evidence, Role, RuntimeEngine, WorkUnit


def run() -> dict[str, object]:
    r = RuntimeEngine()
    r.register_agent(Agent("worker", frozenset({"read", "execute"}), frozenset({"read", "execute"})))
    r.register_role(Role("worker", ("execute",), frozenset({"read", "execute"})))
    failed = WorkUnit("wu-retry-source", "recover failed work", "worker", ("recovery passes",))
    r.create_work_unit(failed)
    r.bind(
        AgentContract(
            "contract-retry-source",
            failed.id,
            "worker",
            "worker",
            frozenset({"read", "execute"}),
            {},
            {},
            ("recovery passes",),
            ("log",),
        )
    )
    r.start(failed.id)
    r.record_evidence(Evidence("e-retry-failure", failed.id, "worker", "log", "failure-1", "fixture"))
    failed.status = "BLOCKED"
    retry = r.retry(failed.id, "recover after runtime failure", ("e-retry-failure",))
    return {
        "failed_work_unit": {
            "id": failed.id,
            "status": failed.status,
            "evidence": sorted(
                ref for ref, evidence in r.evidence.items() if evidence.work_unit_id == failed.id
            ),
        },
        "retry_work_unit": {
            "id": retry.id,
            "parent_id": retry.parent_id,
            "status": retry.status,
            "retry_reason": retry.retry_reason,
            "failure_evidence_refs": retry.failure_evidence_refs,
        },
    }
