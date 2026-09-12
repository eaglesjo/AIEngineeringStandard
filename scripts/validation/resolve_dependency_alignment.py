#!/usr/bin/env python3
"""Deterministic, vendor-neutral dependency compatibility alignment contract.

This harness does not invoke a package manager. It models the minimum decision
boundary required by the 2.0 selected-library policy so implementations can be
tested without network access or package-index side effects.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))

def satisfies(version: str, constraint: str) -> bool:
    value = version_key(version); constraint = constraint.strip()
    if constraint.startswith(">="): return value >= version_key(constraint[2:].strip())
    if constraint.startswith(">"): return value > version_key(constraint[1:].strip())
    if constraint.startswith("<="): return value <= version_key(constraint[2:].strip())
    if constraint.startswith("<"): return value < version_key(constraint[1:].strip())
    if constraint.startswith("=="): return value == version_key(constraint[2:].strip())
    raise ValueError(f"Unsupported constraint: {constraint}")

def resolve_alignment(scenario: dict) -> dict:
    selected = scenario["selected_dependency"]; graph = scenario["dependency_graph"]; candidates = scenario["candidate_versions"]
    selected_name = selected["name"]; selected_version = selected["version"]
    if selected_version not in candidates.get(selected_name, []):
        return {"status": "UNRESOLVED", "reason": "selected version is not a candidate"}
    constraints: list[tuple[str, str]] = []; affected: list[str] = []
    for package, metadata in graph.items():
        if package == selected_name: continue
        for constraint in metadata.get("constraints_from_selected", []):
            constraints.append((package, constraint)); affected.append(package)
    aligned: dict[str, str] = {}
    for package, constraint in constraints:
        current = graph[package]["current_version"]
        compatible = [version for version in candidates.get(package, []) if satisfies(version, constraint)]
        if not compatible:
            return {"status": "UNRESOLVED", "reason": f"no compatible candidate for {package}", "selected_dependency": selected, "affected_dependencies": sorted(set(affected))}
        if satisfies(current, constraint): aligned[package] = current
        else: aligned[package] = min(compatible, key=version_key)
    changes = {package: version for package, version in aligned.items() if version != graph[package]["current_version"]}
    unrelated = set(graph) - set(affected) - {selected_name}
    for package in unrelated:
        expected = scenario.get("expected_unrelated_versions", {}).get(package)
        if expected is not None and graph[package]["current_version"] != expected:
            return {"status": "FAIL", "reason": f"unrelated dependency changed: {package}"}
    return {"status": "RESOLVED", "selected_dependency": selected, "affected_dependencies": sorted(set(affected)), "changes": changes, "unrelated_dependencies_unchanged": sorted(unrelated)}

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("scenario", type=Path); parser.add_argument("--output", type=Path); args = parser.parse_args()
    result = resolve_alignment(json.loads(args.scenario.read_text(encoding="utf-8"))); payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output: args.output.write_text(payload, encoding="utf-8")
    print(payload, end=""); return 0 if result["status"] in {"RESOLVED", "UNRESOLVED"} else 1

if __name__ == "__main__": raise SystemExit(main())
