from core.runtime.v2_1.engine import Evidence, RuntimeEngine, WorkUnit
import pytest


def _runtime():
    runtime = RuntimeEngine()
    runtime.create_work_unit(
        WorkUnit("wu-1", "evidence identity", "planner", ("tests pass",))
    )
    return runtime


def test_evidence_requires_existing_work_unit():
    runtime = RuntimeEngine()
    with pytest.raises(ValueError, match="unknown work unit"):
        runtime.record_evidence(
            Evidence("e-unknown", "missing", "planner", "test-result", "ref", "fixture")
        )


def test_evidence_identity_cannot_be_overwritten():
    runtime = _runtime()
    runtime.record_evidence(
        Evidence("e-1", "wu-1", "planner", "test-result", "first", "fixture")
    )
    with pytest.raises(ValueError, match="evidence already exists"):
        runtime.record_evidence(
            Evidence("e-1", "wu-1", "planner", "log", "second", "fixture")
        )
    assert runtime.evidence["e-1"].reference == "first"


def test_same_evidence_id_cannot_cross_work_units():
    runtime = _runtime()
    runtime.create_work_unit(
        WorkUnit("wu-2", "other", "planner", ("other",))
    )
    runtime.record_evidence(
        Evidence("e-1", "wu-1", "planner", "test-result", "first", "fixture")
    )
    with pytest.raises(ValueError, match="evidence already exists"):
        runtime.record_evidence(
            Evidence("e-1", "wu-2", "planner", "test-result", "second", "fixture")
        )


def test_evidence_record_remains_retrievable_by_identity():
    runtime = _runtime()
    evidence = Evidence(
        "e-1", "wu-1", "planner", "test-result", "first", "fixture"
    )
    runtime.record_evidence(evidence)
    assert runtime.evidence["e-1"] == evidence
