from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = ROOT / "profiles" / "agent"

CHECK_IDS = [
    "instruction-discovery",
    "skill-discovery",
    "skill-loading",
    "plugin-capability",
    "mcp-capability",
    "permission-check",
    "task-execution",
    "validation",
    "failure-recovery",
    "evidence-reporting",
]
VALID_RESULTS = {"PASS", "PARTIAL", "ADAPTER", "UNTESTED", "UNSUPPORTED", "FAIL"}


def make_check(check_id: str, result: str, evidence: str, notes: str | None = None) -> dict[str, str]:
    if check_id not in CHECK_IDS:
        raise ValueError(f"Unknown conformance check id: {check_id}")
    if result not in VALID_RESULTS:
        raise ValueError(f"Invalid conformance check result: {result}")
    item = {"id": check_id, "result": result, "evidence": evidence}
    if notes:
        item["notes"] = notes
    return item


def load_profile(agent_id: str) -> dict:
    path = PROFILE_DIR / f"{agent_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Agent profile not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def static_conformance(agent_id: str) -> dict:
    profile = load_profile(agent_id)
    agent = profile.get("agent", {})
    discovery = profile.get("discovery", {})
    capabilities = profile.get("capabilities", {})
    checks: list[dict[str, str]] = []

    instruction_files = discovery.get("project_instruction_files", [])
    instruction_present = [p for p in instruction_files if (ROOT / p).is_file()]
    checks.append(make_check(
        "instruction-discovery",
        "PASS" if instruction_files and len(instruction_present) == len(instruction_files) else "FAIL",
        ", ".join(instruction_present) or "none",
        "Static path presence only; runtime discovery was not exercised.",
    ))

    skill_locations = discovery.get("portable_skill_locations", [])
    skill_present = [p for p in skill_locations if (ROOT / p).is_dir()]
    checks.append(make_check(
        "skill-discovery",
        "PASS" if skill_locations and len(skill_present) == len(skill_locations) else "FAIL",
        ", ".join(skill_present) or "none",
        "Static path presence only; runtime discovery was not exercised.",
    ))

    skill_root = ROOT / ".agents" / "skills"
    skill_files = list(skill_root.glob("*/SKILL.md")) if skill_root.is_dir() else []
    checks.append(make_check(
        "skill-loading",
        "PASS" if skill_files else "UNTESTED",
        "; ".join(str(p.relative_to(ROOT)) for p in skill_files) or "No portable Skill fixture discovered",
        "Static discovery only; the agent runtime was not invoked.",
    ))

    for check_id, capability_key in (("plugin-capability", "plugins"), ("mcp-capability", "mcp")):
        declared = capabilities.get(capability_key, "UNTESTED")
        result = declared if declared in VALID_RESULTS else "UNTESTED"
        checks.append(make_check(
            check_id,
            result,
            f"Profile capability declaration: {declared}",
            "Runtime capability is not exercised by the static runner.",
        ))

    checks.extend([
        make_check("permission-check", "UNTESTED", "Agent runtime permissions were not exercised."),
        make_check("task-execution", "UNTESTED", "No agent runtime was invoked; arbitrary Skill/plugin code is never executed."),
        make_check("validation", "PASS", "Static profile and discovery contract validated by this runner."),
        make_check("failure-recovery", "UNTESTED", "Requires runtime-level fault injection and recovery evidence."),
        make_check("evidence-reporting", "PASS", "Machine-readable conformance result generated from deterministic checks."),
    ])

    overall = "FAIL" if any(check["result"] == "FAIL" for check in checks) else "UNTESTED"
    return {
        "schema_version": "2.0.0",
        "standard_version": str(profile.get("standard_version", "2.0")),
        "agent": str(agent.get("id", agent_id)),
        "runtime_version": profile.get("runtime", {}).get("version"),
        "tested_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "result": overall,
        "checks": checks,
    }


def validate_result(result: dict) -> None:
    required = {"schema_version", "standard_version", "agent", "tested_at", "result", "checks"}
    missing = required - result.keys()
    if missing:
        raise ValueError(f"Conformance result missing fields: {sorted(missing)}")
    if result["schema_version"] != "2.0.0":
        raise ValueError("Conformance result schema_version must be 2.0.0")
    if result["result"] not in VALID_RESULTS:
        raise ValueError("Invalid conformance result")
    ids = [item.get("id") for item in result["checks"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate conformance check ids")
    missing_checks = set(CHECK_IDS) - set(ids)
    if missing_checks:
        raise ValueError(f"Missing conformance checks: {sorted(missing_checks)}")
    for item in result["checks"]:
        if item.get("result") not in VALID_RESULTS:
            raise ValueError(f"Invalid check result for {item.get('id')}: {item.get('result')}")
    expected_overall = "FAIL" if any(item["result"] == "FAIL" for item in result["checks"]) else "UNTESTED"
    if result["result"] != expected_overall:
        raise ValueError(f"Overall result {result['result']} does not match static check results; expected {expected_overall}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic AIEngineeringStandard 2.0 static conformance checks.")
    parser.add_argument("--agent", default="codex", help="Agent profile id under profiles/agent")
    parser.add_argument("--output", help="Write the result JSON to this path; stdout is always emitted")
    parser.add_argument("--check-only", action="store_true", help="Run checks and exit non-zero when a static contract check fails")
    args = parser.parse_args()

    result = static_conformance(args.agent)
    validate_result(result)
    print(json.dumps(result, indent=2))
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Conformance result written: {output}")
    return 1 if args.check_only and result["result"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
