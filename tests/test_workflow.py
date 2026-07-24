import tempfile
import unittest
from pathlib import Path

from polymathica_hackathon.workflow import run_workflow


class WorkflowTests(unittest.TestCase):
    def test_workflow_generates_required_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_workflow(Path(tmp))

            self.assertEqual(result.validation_status, "passed")
            self.assertTrue(result.report_path.exists())
            self.assertTrue(result.archive_manifest_path.exists())
            self.assertTrue(result.provenance_path.exists())
            self.assertTrue(result.visualization_path.exists())

    def test_workflow_is_deterministic_enough_for_replay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            first = run_workflow(base / "first")
            second = run_workflow(base / "second")

            self.assertEqual(
                (first.output_dir / "validation_report.json").read_text(),
                (second.output_dir / "validation_report.json").read_text(),
            )
            self.assertEqual(
                (first.output_dir / "replay_samples.json").read_text(),
                (second.output_dir / "replay_samples.json").read_text(),
            )


if __name__ == "__main__":
    unittest.main()
