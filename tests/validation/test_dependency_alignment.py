#!/usr/bin/env python3
"""Deterministic tests for the 2.0 selected-library compatibility contract."""
from __future__ import annotations
import importlib.util, json, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "validation" / "resolve_dependency_alignment.py"
FIXTURE_PATH = ROOT / "tests" / "validation" / "fixtures" / "dependency-alignment-selected-library.json"
def load_module():
    spec = importlib.util.spec_from_file_location("dependency_alignment_test", MODULE_PATH)
    if spec is None or spec.loader is None: raise ImportError(f"Cannot load resolver: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module); return module
def load_fixture() -> dict: return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
class DependencyAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None: cls.module = load_module()
    def test_selected_library_is_preserved_and_affected_dependency_aligns(self) -> None:
        result = self.module.resolve_alignment(load_fixture()); self.assertEqual(result["status"], "RESOLVED"); self.assertEqual(result["selected_dependency"]["version"], "2.0.0"); self.assertEqual(result["affected_dependencies"], ["compat-lib"]); self.assertEqual(result["changes"], {"compat-lib": "2.0.0"}); self.assertEqual(result["unrelated_dependencies_unchanged"], ["unrelated-lib"])
    def test_unresolved_when_selected_version_is_not_a_candidate(self) -> None:
        scenario = load_fixture(); scenario["candidate_versions"]["anchor-lib"].remove("2.0.0"); result = self.module.resolve_alignment(scenario); self.assertEqual(result["status"], "UNRESOLVED"); self.assertIn("selected version is not a candidate", result["reason"])
    def test_unresolved_when_affected_dependency_has_no_compatible_candidate(self) -> None:
        scenario = load_fixture(); scenario["candidate_versions"]["compat-lib"] = ["1.0.0"]; result = self.module.resolve_alignment(scenario); self.assertEqual(result["status"], "UNRESOLVED"); self.assertIn("no compatible candidate for compat-lib", result["reason"]); self.assertEqual(result["selected_dependency"]["version"], "2.0.0")
    def test_unrelated_dependency_drift_is_rejected(self) -> None:
        scenario = load_fixture(); scenario["dependency_graph"]["unrelated-lib"]["current_version"] = "5.0.0"; result = self.module.resolve_alignment(scenario); self.assertEqual(result["status"], "FAIL"); self.assertIn("unrelated dependency changed: unrelated-lib", result["reason"])
    def test_compatible_current_affected_dependency_is_preserved(self) -> None:
        scenario = load_fixture(); scenario["dependency_graph"]["compat-lib"]["current_version"] = "2.1.0"; result = self.module.resolve_alignment(scenario); self.assertEqual(result["status"], "RESOLVED"); self.assertEqual(result["changes"], {})
    def test_supported_constraints_are_deterministic(self) -> None:
        for version, constraint, expected in [("2.0.0", ">=2.0.0", True), ("2.1.0", ">2.0.0", True), ("2.0.0", "<=2.0.0", True), ("1.9.0", "<2.0.0", True), ("2.0.0", "==2.0.0", True), ("1.9.0", ">=2.0.0", False)]:
            with self.subTest(version=version, constraint=constraint): self.assertEqual(self.module.satisfies(version, constraint), expected)
if __name__ == "__main__": unittest.main()
