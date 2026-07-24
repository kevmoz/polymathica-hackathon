import tempfile
import unittest
from pathlib import Path

from polymathica_hackathon.workflow import (
    GovernanceError,
    REQUIRED_STAGES,
    WorkflowConfigurationError,
    build_archive_manifest,
    configured_experiment,
    read_json,
    replay_field,
    run_workflow,
    validate,
    validate_config,
    verify_artifact_hashes,
)


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

    def test_invalid_configuration_is_rejected(self) -> None:
        config = configured_experiment()
        config["parameters"]["dt"] = 0.0

        with self.assertRaises(WorkflowConfigurationError):
            validate_config(config)

    def test_public_demo_rejects_live_solver_claim(self) -> None:
        config = configured_experiment()
        config["mode"] = "live_solver"

        with self.assertRaises(WorkflowConfigurationError):
            run_workflow(Path("unused"), config=config)

    def test_failed_validation_blocks_archive_manifest(self) -> None:
        failed_validation = {"status": "failed"}

        with self.assertRaises(GovernanceError):
            build_archive_manifest("workflow", failed_validation, "abc123")

    def test_artifact_hashes_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_workflow(Path(tmp))

            self.assertTrue(verify_artifact_hashes(result.provenance_path))

    def test_artifact_hash_mismatch_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_workflow(Path(tmp))
            (result.output_dir / "report.html").write_text("tampered", encoding="utf-8")

            with self.assertRaises(GovernanceError):
                verify_artifact_hashes(result.provenance_path)

    def test_missing_artifact_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_workflow(Path(tmp))
            (result.output_dir / "report.html").unlink()

            with self.assertRaises(FileNotFoundError):
                verify_artifact_hashes(result.provenance_path)

    def test_replay_output_schema_is_complete(self) -> None:
        samples = replay_field(configured_experiment())

        self.assertGreater(len(samples), 2)
        for row in samples:
            self.assertEqual(
                set(row),
                {"step", "time", "kinetic_energy", "enstrophy", "divergence_l2"},
            )

    def test_validation_schema_is_complete(self) -> None:
        validation = validate(replay_field(configured_experiment()))

        self.assertEqual(validation["schema"], "polymathica.validation.v1")
        self.assertEqual(validation["status"], "passed")
        self.assertEqual(len(validation["gates"]), 4)
        for gate in validation["gates"]:
            self.assertEqual(set(gate), {"name", "measured", "expected", "tolerance", "passed"})

    def test_provenance_schema_lists_required_stages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_workflow(Path(tmp))
            provenance = read_json(result.provenance_path)

            self.assertEqual(provenance["schema"], "polymathica.provenance.v1")
            self.assertEqual(provenance["stages"], REQUIRED_STAGES)
            self.assertIn("validation_report.json", provenance["artifacts"])


if __name__ == "__main__":
    unittest.main()
