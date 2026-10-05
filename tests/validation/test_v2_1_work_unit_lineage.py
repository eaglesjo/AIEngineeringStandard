from core.runtime.v2_1.engine import Agent, RuntimeEngine, WorkUnit
import pytest


def _runtime() -> RuntimeEngine:
    runtime = RuntimeEngine()
    runtime.register_agent(
        Agent("planner", frozenset({"read"}), frozenset({"read"}))
    )
    runtime.register_agent(
        Agent("implementer", frozenset({"read", "execute"}), frozenset({"read", "execute"}))
    )
    return runtime


def test_work_unit_owner_must_be_registered():
    runtime = _runtime()
    with pytest.raises(ValueError, match="owner agent is not registered"):
        runtime.create_work_unit(
            WorkUnit("wu-owner", "invalid owner", "unknown", ("done",))
        )


def test_work_unit_parent_must_exist():
    runtime = _runtime()
    with pytest.raises(ValueError, match="parent does not exist"):
        runtime.create_work_unit(
            WorkUnit("wu-child", "invalid parent", "implementer", ("done",), parent_id="missing")
        )


def test_work_unit_cannot_be_its_own_parent():
    runtime = _runtime()
    with pytest.raises(ValueError, match="cannot be its own parent"):
        runtime.create_work_unit(
            WorkUnit("wu-self", "invalid lineage", "implementer", ("done",), parent_id="wu-self")
        )


def test_parallel_child_may_reference_existing_parent():
    runtime = _runtime()
    runtime.create_work_unit(
        WorkUnit("wu-root", "root", "planner", ("done",))
    )
    runtime.create_work_unit(
        WorkUnit("wu-child", "child", "implementer", ("done",), parent_id="wu-root")
    )
    assert runtime.work_units["wu-child"].parent_id == "wu-root"
