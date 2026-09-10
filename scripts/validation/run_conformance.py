from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = ROOT / "profiles" / "agent"
OUTPUT_DIR = ROOT / "tests" / "validation" / "fixtures" / "conformance"

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


def check(result: str, evidence: str, notes: str | None = None) -> dict[str, str]:
    item = {"id": result if False else "", "result": ""}
    item["result"] = evidence  # overwritten by caller; keeps construction explicit
    raise AssertionError("check() must be called through make_check")


def make_check(check_id: str, result: str, evidence: str, notes: str | None = None) -> dict[str, str]:
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
    if instruction_files and len(instruction_present) == len(instruction_files):
        checks.append(make_check("instruction-discovery", "PASS", ", ".join(instruction_present)))
    else:
        checks.append(make_check("instruction-discovery", "FAIL", ", ".join(instruction_present) or "none"))

    skill_locations = discovery.get("portable_skill_locations", [])
    skill_present = [p for p in skill_locations if (ROOT / p).is_dir()]
    if skill_locations and len(skill_present) == len(skill_locations):
        checks.append(make_check("skill-discovery", "PASS", ", ".join(skill_present)))
    else:
        checks.append(make_check("skill-discovery", "FAIL", ", ".join(skill_present) or "none"))

    skill_files = list((ROOT / ".agents" / "skills").glob("*/SKILL.md")) if (ROOT / ".agents" / "skills").is_dir() else []
    checks.append(make_check(
        "skill-loading",
        "PASS" if skill_files else "UNTESTED",
        "; ".join(str(p.relative_to(ROOT)) for p in skill_files) or "No portable Skill fixture discovered",
        "Static discovery only; the agent runtime was not invoked.",
    ))

    for check_id, capability_key in (("plugin-capability", "plugins"), ("mcp-capability", "mcp")):
        declared = capabilities.get(capability_key, "UNTESTED")
        checks.append(make_check(
            check_id,
            declared if declared in {"PASS", "PARTIAL", "ADAPTER", "UNTESTED", "UNSUPPORTED"} else "UNTESTED",
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

    return {
        "schema_version": "2.0.0",
        "standard_version": str(profile.get("standard_version", "2.0")),
        "agent": str(agent.get("id", agent_id)),
        "runtime_version": profile.get("runtime", {}).get("version"),
        "tested_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "result": "UNTESTED",
        "checks": checks,
    }


def validate_result(result: dict) -> None:
    required = {"schema_version", "standard_version", "agent", "tested_at", "result", "checks"}
    missing = required - result.keys()
    if missing:
        raise ValueError(f"Conformance result missing fields: {sorted(missing)}")
    if result["schema_version"] != "2.0.0":
        raise ValueError("Conformance result schema_version must be 2.0.0")
    if result["result"] not in {"PASS", "PARTIAL", "ADAPTER", "UNTESTED", "UNSUPPORTED"}:
        raise ValueError("Invalid conformance result")
    ids = {item.get("id") for item in result["checks"]}
    missing_checks = set(CHECK_IDS) - ids
    if missing_checks:
        raise ValueError(f"Missing conformance checks: {sorted(missing_checks)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic AIEngineeringStandard 2.0 static conformance checks.")
    parser.add_argument("--agent", default="codex", help="Agent profile id under profiles/agent")
    parser.add_argument("--output", help="Write the result JSON to this path")
    args = parser.parse_args()

    result = static_conformance(args.agent)
    validate_result(result)
    output = Path(args.output) if args.output else OUTPUT_DIR / f"{args.agent}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"Conformance result written: {output.relative_to(ROOT) if output.is_relative_to(ROOT) else output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
