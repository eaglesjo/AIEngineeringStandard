from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "core/validation/dependency-conflict-resolution-policy.md"
AGENTS = ROOT / "AGENTS.md"
COMMON_AGENT = ROOT / "core/common/AGENT.md"


def require(text: str, *terms: str) -> None:
    missing = [term for term in terms if term not in text]
    assert not missing, f"Missing policy requirements: {missing}"


def main() -> None:
    policy = POLICY.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    common_agent = COMMON_AGENT.read_text(encoding="utf-8")

    require(
        policy,
        "compatibility anchor",
        "selected dependency",
        "affected dependency",
        "transitive dependency",
        "compatibility constraint",
        "authoritative package metadata",
        "dependency graph",
        "determine a compatible version set",
        "preserve the developer's selected library/version",
        "minimum compatible change",
        "broad or unexplained upgrades/downgrades",
        "installation/resolution",
        "smoke testing",
        "regression testing",
        "Lock the resolved state",
        "record the selected dependency",
    )

    lifecycle = "Select → Discover → Analyze → Detect → Measure → Resolve → Align → Smoke Test → Lock → Implement → Validate → Record"
    assert lifecycle in policy

    acceptance = policy[policy.index("## Minimum acceptance criteria") :]
    require(
        acceptance,
        "If a developer-selected dependency exists",
        "compatibility constraints were analyzed",
        "proactively compatibility-checked",
        "final environment is reproducible",
        "result and evidence are recorded",
    )

    reference = "core/validation/dependency-conflict-resolution-policy.md"
    assert reference in agents
    assert reference in common_agent

    print("dependency conflict resolution policy: PASS")
    print("selected-library compatibility alignment: PASS")
    print("agent policy references: PASS")


if __name__ == "__main__":
    main()
