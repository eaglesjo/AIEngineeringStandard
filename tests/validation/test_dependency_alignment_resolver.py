#!/usr/bin/env python3
"""Executable contract tests for selected-library compatibility alignment."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validation.resolve_dependency_alignment import resolve_alignment


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/validation/fixtures/dependency-alignment-selected-library.json"


class DependencyAlignmentResolverTests(unittest.TestCase):
    def load(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_selected_library_is_anchor_and_only_affected_dependency_changes(self):
        scenario = self.load()
        result = resolve_alignment(scenario)

        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(result["selected_dependency"]["version"], "2.0.0")
        self.assertEqual(result["changes"], {"compat-lib": "2.0.0"})
        self.assertEqual(result["unrelated_dependencies_unchanged"], ["unrelated-lib"])

    def test_incompatible_anchor_is_reported_not_replaced(self):
        scenario = self.load()
        scenario["dependency_graph"]["compat-lib"]["constraints_from_selected"] = [">=3.0.0"]
        result = resolve_alignment(scenario)

        self.assertEqual(result["status"], "UNRESOLVED")
        self.assertEqual(result["selected_dependency"]["version"], "2.0.0")
        self.assertIn("compat-lib", result["affected_dependencies"])

    def test_unrelated_dependency_drift_is_rejected(self):
        scenario = self.load()
        scenario["expected_unrelated_versions"]["unrelated-lib"] = "4.3.0"
        result = resolve_alignment(scenario)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("unrelated dependency changed", result["reason"])


if __name__ == "__main__":
    unittest.main()
