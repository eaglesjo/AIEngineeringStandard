from tests.fixtures.v2_1_multi_agent_e2e import run

def test_canonical_multi_agent_e2e():
    result = run()
    assert result["work_units"] == {"wu-root": "ACCEPTED", "wu-implementation": "HANDOFF_PENDING", "wu-verification": "ACCEPTED"}
    assert result["evidence"] == ["e-implementation", "e-root", "e-tests", "e-verification"]
    assert result["handoffs"] == ["h-implementation", "h-verification"]
    assert result["evaluations"] == ["eval-root", "eval-verification"]
