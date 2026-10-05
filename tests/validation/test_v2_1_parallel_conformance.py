from tests.fixtures.v2_1_parallel_conformance import run

def test_parallel_conformance_requires_explicit_join_boundary():
    result = run()
    assert result["work_units"] == {"wu-parallel-root": "ACCEPTED", "wu-parallel-a": "ACCEPTED", "wu-parallel-b": "ACCEPTED"}
    assert result["parents"] == {"wu-parallel-a": "wu-parallel-root", "wu-parallel-b": "wu-parallel-root"}
    assert result["evaluations"] == ["eval-parallel-a", "eval-parallel-b", "eval-parallel-root"]
    assert result["join_evidence"] == ["e-parallel-join"]
