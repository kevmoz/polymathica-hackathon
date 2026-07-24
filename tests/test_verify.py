import tempfile
import unittest
from pathlib import Path

from polymathica_hackathon.suite import run_evidence_suite
from polymathica_hackathon.verify import verify_evidence_bundle
from polymathica_hackathon.workflow import GovernanceError, read_json, write_json


class EvidenceVerificationTests(unittest.TestCase):
    def test_verifier_accepts_fresh_evidence_suite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_evidence_suite(root)
            result = verify_evidence_bundle(root, report_path=root / "verification_report.json")

            self.assertEqual(result.status, "passed")
            self.assertEqual(result.artifacts_checked, 8)
            self.assertEqual(result.components_checked, 4)
            self.assertTrue((root / "verification_report.json").exists())

    def test_verifier_rejects_tampered_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_evidence_suite(root)
            (root / "poiseuille" / "poiseuille_validation.json").write_text("tampered", encoding="utf-8")

            with self.assertRaises(GovernanceError):
                verify_evidence_bundle(root)

    def test_verifier_rejects_failed_summary_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_evidence_suite(root)
            summary_path = root / "evidence_suite_summary.json"
            summary = read_json(summary_path)
            summary["status"] = "failed"
            write_json(summary_path, summary)

            with self.assertRaises(GovernanceError):
                verify_evidence_bundle(root)

    def test_verifier_rejects_missing_component(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_evidence_suite(root)
            summary_path = root / "evidence_suite_summary.json"
            summary = read_json(summary_path)
            del summary["components"]["projection"]
            write_json(summary_path, summary)

            with self.assertRaises(GovernanceError):
                verify_evidence_bundle(root)


if __name__ == "__main__":
    unittest.main()
