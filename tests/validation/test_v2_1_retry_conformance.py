from tests.fixtures.v2_1_retry_conformance import run

def test_retry_conformance_preserves_failed_attempt_provenance():
    result = run()
    assert result["failed_work_unit"]["status"] == "BLOCKED"
    retry = result["retry_work_unit"]
    assert retry["parent_id"] == "wu-retry-source"
    assert retry["retry_reason"] == "recover after runtime failure"
    assert retry["failure_evidence_refs"] == ("e-retry-failure",)
