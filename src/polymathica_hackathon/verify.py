"""Independent verification for the public evidence bundle."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .workflow import GovernanceError, read_json, sha256_bytes, verify_artifact_hashes, write_json

DEFAULT_EVIDENCE_ROOT = Path("demo")
REQUIRED_COMPONENTS = {"workflow", "taylor_green", "projection", "poiseuille"}


@dataclass(frozen=True)
class VerificationResult:
    evidence_root: Path
    status: str
    artifacts_checked: int
    components_checked: int
    report_path: Path | None


def verify_hashes(root: Path, manifest: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for relative_path, expected_hash in manifest["artifacts"].items():
        artifact_path = root / relative_path
        if not artifact_path.exists():
            raise FileNotFoundError(str(artifact_path))
        actual_hash = sha256_bytes(artifact_path.read_bytes())
        if actual_hash != expected_hash:
            raise GovernanceError(f"evidence suite artifact hash mismatch: {relative_path}")
        rows.append({"artifact": relative_path, "sha256": actual_hash, "status": "passed"})
    return rows


def verify_component_statuses(root: Path, summary: dict[str, Any]) -> dict[str, str]:
    components = summary.get("components", {})
    missing = REQUIRED_COMPONENTS.difference(components)
    if missing:
        raise GovernanceError(f"evidence suite summary is missing components: {sorted(missing)}")

    statuses = {}
    for name in sorted(REQUIRED_COMPONENTS):
        component = components[name]
        status = component.get("status")
        if status != "passed":
            raise GovernanceError(f"component did not pass: {name}")
        statuses[name] = status

    validation_files = [
        root / "output" / "validation_report.json",
        root / "benchmark" / "benchmark_validation.json",
        root / "projection" / "projection_validation.json",
        root / "poiseuille" / "poiseuille_validation.json",
    ]
    for path in validation_files:
        validation = read_json(path)
        if validation.get("status") != "passed":
            raise GovernanceError(f"validation artifact did not pass: {path}")
    return statuses


def verify_evidence_bundle(root: Path = DEFAULT_EVIDENCE_ROOT, *, report_path: Path | None = None) -> VerificationResult:
    manifest_path = root / "evidence_suite_manifest.json"
    summary_path = root / "evidence_suite_summary.json"
    manifest = read_json(manifest_path)
    summary = read_json(summary_path)

    if manifest.get("schema") != "polymathica.evidence_suite.manifest.v1":
        raise GovernanceError("unexpected evidence suite manifest schema")
    if summary.get("schema") != "polymathica.evidence_suite.summary.v1":
        raise GovernanceError("unexpected evidence suite summary schema")
    if manifest.get("status") != "passed" or summary.get("status") != "passed":
        raise GovernanceError("evidence suite did not pass")

    artifact_rows = verify_hashes(root, manifest)
    component_statuses = verify_component_statuses(root, summary)
    verify_artifact_hashes(root / "output" / "provenance.json")

    report = {
        "schema": "polymathica.evidence_verification.report.v1",
        "status": "passed",
        "evidence_root": str(root),
        "artifacts_checked": len(artifact_rows),
        "components_checked": len(component_statuses),
        "components": component_statuses,
        "artifacts": artifact_rows,
    }
    if report_path is not None:
        write_json(report_path, report)
    return VerificationResult(
        evidence_root=root,
        status="passed",
        artifacts_checked=len(artifact_rows),
        components_checked=len(component_statuses),
        report_path=report_path,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the committed POLYMATHICA public evidence bundle.")
    parser.add_argument("--root", default=str(DEFAULT_EVIDENCE_ROOT), help="Evidence root directory.")
    parser.add_argument("--report", default="", help="Optional JSON verification report path.")
    args = parser.parse_args()
    report_path = Path(args.report) if args.report else None
    result = verify_evidence_bundle(Path(args.root), report_path=report_path)
    print(f"Evidence verification: {result.status}")
    print(f"Artifacts checked: {result.artifacts_checked}")
    print(f"Components checked: {result.components_checked}")
    if result.report_path is not None:
        print(f"Report: {result.report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
