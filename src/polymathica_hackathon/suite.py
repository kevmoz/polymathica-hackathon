"""End-to-end public evidence suite for reviewer verification."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .benchmark import run_benchmark
from .poiseuille import run_poiseuille_benchmark
from .projection import run_projection_benchmark
from .workflow import sha256_bytes, verify_artifact_hashes, write_json, run_workflow

DEFAULT_SUITE_DIR = Path("demo")


@dataclass(frozen=True)
class EvidenceSuiteResult:
    output_dir: Path
    status: str
    workflow_status: str
    taylor_green_status: str
    projection_status: str
    poiseuille_status: str
    tests_expected: int
    summary_path: Path
    manifest_path: Path


def artifact_hash(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run_evidence_suite(output_dir: Path = DEFAULT_SUITE_DIR) -> EvidenceSuiteResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    workflow = run_workflow(output_dir / "output")
    taylor_green = run_benchmark(output_dir / "benchmark")
    projection = run_projection_benchmark(output_dir / "projection")
    poiseuille = run_poiseuille_benchmark(output_dir / "poiseuille")
    verify_artifact_hashes(workflow.provenance_path)

    statuses = {
        "workflow": workflow.validation_status,
        "taylor_green": taylor_green.status,
        "projection": projection.status,
        "poiseuille": poiseuille.status,
    }
    status = "passed" if all(value == "passed" for value in statuses.values()) else "failed"
    summary: dict[str, Any] = {
        "schema": "polymathica.evidence_suite.summary.v1",
        "status": status,
        "scope": "public demonstration package for the broader POLYMATHICA ecosystem",
        "components": {
            "workflow": {
                "status": workflow.validation_status,
                "report": "output/report.html",
                "provenance": "output/provenance.json",
                "archive_manifest": "output/archive_manifest.json",
            },
            "taylor_green": {
                "status": taylor_green.status,
                "l2_error": taylor_green.l2_error,
                "energy_relative_error": taylor_green.energy_relative_error,
                "max_divergence_l2": taylor_green.max_divergence_l2,
                "observed_order": taylor_green.observed_order,
                "validation": "benchmark/benchmark_validation.json",
            },
            "projection": {
                "status": projection.status,
                "divergence_before_l2": projection.divergence_before,
                "divergence_after_l2": projection.divergence_after,
                "projected_l2_error": projection.projected_l2_error,
                "validation": "projection/projection_validation.json",
            },
            "poiseuille": {
                "status": poiseuille.status,
                "l2_error": poiseuille.l2_error,
                "flow_rate_error": poiseuille.flow_rate_error,
                "wall_shear_error": poiseuille.wall_shear_error,
                "observed_order": poiseuille.observed_order,
                "validation": "poiseuille/poiseuille_validation.json",
            },
        },
        "reviewer_commands": [
            "python -m polymathica_hackathon.suite --output demo",
            "python -m unittest discover -s tests",
        ],
    }
    summary_path = output_dir / "evidence_suite_summary.json"
    write_json(summary_path, summary)

    artifacts = {
        "evidence_suite_summary.json": artifact_hash(summary_path),
        "output/provenance.json": artifact_hash(output_dir / "output" / "provenance.json"),
        "output/archive_manifest.json": artifact_hash(output_dir / "output" / "archive_manifest.json"),
        "benchmark/benchmark_validation.json": artifact_hash(output_dir / "benchmark" / "benchmark_validation.json"),
        "benchmark/convergence_study.json": artifact_hash(output_dir / "benchmark" / "convergence_study.json"),
        "projection/projection_validation.json": artifact_hash(output_dir / "projection" / "projection_validation.json"),
        "poiseuille/poiseuille_validation.json": artifact_hash(output_dir / "poiseuille" / "poiseuille_validation.json"),
        "poiseuille/poiseuille_convergence.json": artifact_hash(output_dir / "poiseuille" / "poiseuille_convergence.json"),
    }
    manifest_path = output_dir / "evidence_suite_manifest.json"
    write_json(
        manifest_path,
        {
            "schema": "polymathica.evidence_suite.manifest.v1",
            "status": status,
            "artifacts": artifacts,
        },
    )
    return EvidenceSuiteResult(
        output_dir=output_dir,
        status=status,
        workflow_status=workflow.validation_status,
        taylor_green_status=taylor_green.status,
        projection_status=projection.status,
        poiseuille_status=poiseuille.status,
        tests_expected=30,
        summary_path=summary_path,
        manifest_path=manifest_path,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the complete public POLYMATHICA evidence suite.")
    parser.add_argument("--output", default=str(DEFAULT_SUITE_DIR), help="Directory for all generated evidence artifacts.")
    args = parser.parse_args()
    result = run_evidence_suite(Path(args.output))
    print(f"Evidence suite: {result.status}")
    print(f"Workflow: {result.workflow_status}")
    print(f"Taylor-Green: {result.taylor_green_status}")
    print(f"Projection: {result.projection_status}")
    print(f"Poiseuille: {result.poiseuille_status}")
    print(f"Summary: {result.summary_path}")
    print(f"Manifest: {result.manifest_path}")
    return 0 if result.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
