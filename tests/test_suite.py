import tempfile
import unittest
from pathlib import Path

from polymathica_hackathon.suite import run_evidence_suite
from polymathica_hackathon.workflow import read_json, sha256_bytes


class EvidenceSuiteTests(unittest.TestCase):
    def test_evidence_suite_runs_all_public_components(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_evidence_suite(Path(tmp))

            self.assertEqual(result.status, "passed")
            self.assertEqual(result.workflow_status, "passed")
            self.assertEqual(result.taylor_green_status, "passed")
            self.assertEqual(result.projection_status, "passed")
            self.assertEqual(result.poiseuille_status, "passed")
            self.assertEqual(result.tests_expected, 34)
            self.assertTrue(result.summary_path.exists())
            self.assertTrue(result.manifest_path.exists())

    def test_evidence_suite_summary_has_reviewer_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_evidence_suite(Path(tmp))
            summary = read_json(result.summary_path)

            self.assertEqual(summary["schema"], "polymathica.evidence_suite.summary.v1")
            self.assertEqual(summary["status"], "passed")
            self.assertEqual(
                set(summary["components"]),
                {"workflow", "taylor_green", "projection", "poiseuille"},
            )
            self.assertIn("public demonstration package", summary["scope"])

    def test_evidence_suite_manifest_hashes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_evidence_suite(Path(tmp))
            manifest = read_json(result.manifest_path)

            self.assertEqual(manifest["schema"], "polymathica.evidence_suite.manifest.v1")
            self.assertEqual(manifest["status"], "passed")
            self.assertEqual(
                manifest["artifacts"]["evidence_suite_summary.json"],
                sha256_bytes(result.summary_path.read_bytes()),
            )


if __name__ == "__main__":
    unittest.main()
