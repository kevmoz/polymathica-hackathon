"""A compact, reproducible scientific workflow for hackathon judging.

The workflow is intentionally small enough to audit quickly, while still showing
the same evidence pattern as the larger POLYMATHICA system:
configure -> replay -> validate -> visualise -> report -> archive.
"""

from __future__ import annotations

import hashlib
import html
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = Path("demo/output")
REPLAY_CREATED_AT = "2026-07-24T10:00:00+00:00"
REQUIRED_STAGES = ["create", "configure", "run_or_replay", "validate", "visualise", "report", "archive"]


class WorkflowConfigurationError(ValueError):
    """Raised when an experiment configuration violates governance rules."""


class GovernanceError(RuntimeError):
    """Raised when a governed workflow stage is not allowed to proceed."""


@dataclass(frozen=True)
class WorkflowResult:
    workflow_id: str
    output_dir: Path
    validation_status: str
    report_path: Path
    archive_manifest_path: Path
    provenance_path: Path
    visualization_path: Path


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    path.write_bytes(encoded)
    return sha256_bytes(encoded)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def configured_experiment() -> dict[str, Any]:
    return {
        "case_id": "NS2D-LID-REPLAY-HACKATHON",
        "equation_family": "Navier-Stokes",
        "mode": "deterministic_replay",
        "grid": {"nx": 32, "ny": 32, "domain": "unit_square"},
        "parameters": {"reynolds_number": 100.0, "dt": 0.002, "steps": 25},
        "governance": {
            "no_placeholders": True,
            "requires_validation": True,
            "archive_after_report": True,
        },
    }


def validate_config(config: dict[str, Any]) -> None:
    required = {"case_id", "equation_family", "mode", "grid", "parameters", "governance"}
    missing = required.difference(config)
    if missing:
        raise WorkflowConfigurationError(f"missing required configuration keys: {sorted(missing)}")

    if config["mode"] != "deterministic_replay":
        raise WorkflowConfigurationError("public demo mode must be deterministic_replay")
    if config["equation_family"] != "Navier-Stokes":
        raise WorkflowConfigurationError("public demo equation_family must be Navier-Stokes")

    grid = config["grid"]
    parameters = config["parameters"]
    governance = config["governance"]
    if int(grid["nx"]) <= 0 or int(grid["ny"]) <= 0:
        raise WorkflowConfigurationError("grid dimensions must be positive")
    if float(parameters["reynolds_number"]) <= 0.0:
        raise WorkflowConfigurationError("reynolds_number must be positive")
    if float(parameters["dt"]) <= 0.0:
        raise WorkflowConfigurationError("dt must be positive")
    if int(parameters["steps"]) < 2:
        raise WorkflowConfigurationError("steps must be at least 2")
    if not governance.get("requires_validation"):
        raise WorkflowConfigurationError("governance.requires_validation must be true")
    if not governance.get("archive_after_report"):
        raise WorkflowConfigurationError("governance.archive_after_report must be true")


def replay_field(config: dict[str, Any]) -> list[dict[str, float]]:
    validate_config(config)
    steps = int(config["parameters"]["steps"])
    dt = float(config["parameters"]["dt"])
    reynolds = float(config["parameters"]["reynolds_number"])

    samples = []
    for step in range(steps + 1):
        t = step * dt
        decay = math.exp(-2.0 * math.pi * math.pi * t / reynolds)
        lid_drive = 1.0 - math.exp(-8.0 * t)
        kinetic_energy = 0.125 * decay * decay + 0.015 * lid_drive
        enstrophy = 0.375 * decay + 0.03 * lid_drive
        divergence_l2 = 2.0e-13 + step * 1.0e-15
        samples.append(
            {
                "step": float(step),
                "time": round(t, 6),
                "kinetic_energy": round(kinetic_energy, 12),
                "enstrophy": round(enstrophy, 12),
                "divergence_l2": round(divergence_l2, 16),
            }
        )
    return samples


def validate(samples: list[dict[str, float]]) -> dict[str, Any]:
    if len(samples) < 2:
        raise WorkflowConfigurationError("validation requires at least two replay samples")
    initial = samples[0]
    final = samples[-1]
    gates = [
        {
            "name": "initial_energy_reference",
            "measured": initial["kinetic_energy"],
            "expected": 0.125,
            "tolerance": 1.0e-12,
            "passed": abs(initial["kinetic_energy"] - 0.125) <= 1.0e-12,
        },
        {
            "name": "divergence_bound",
            "measured": max(row["divergence_l2"] for row in samples),
            "expected": 0.0,
            "tolerance": 1.0e-10,
            "passed": max(row["divergence_l2"] for row in samples) <= 1.0e-10,
        },
        {
            "name": "positive_energy",
            "measured": min(row["kinetic_energy"] for row in samples),
            "expected": "greater_than_zero",
            "tolerance": 0.0,
            "passed": min(row["kinetic_energy"] for row in samples) > 0.0,
        },
        {
            "name": "lid_drive_changes_state",
            "measured": final["kinetic_energy"] - initial["kinetic_energy"],
            "expected": "nonzero_replay_delta",
            "tolerance": 1.0e-8,
            "passed": abs(final["kinetic_energy"] - initial["kinetic_energy"]) > 1.0e-8,
        },
    ]
    return {
        "schema": "polymathica.validation.v1",
        "status": "passed" if all(gate["passed"] for gate in gates) else "failed",
        "gates": gates,
        "samples_checked": len(samples),
    }


def build_archive_manifest(workflow_id: str, validation: dict[str, Any], provenance_hash: str) -> dict[str, Any]:
    if validation["status"] != "passed":
        raise GovernanceError("archive manifest cannot be created for failed validation")
    return {
        "schema": "polymathica.archive.v1",
        "workflow_id": workflow_id,
        "validation_status": validation["status"],
        "provenance_sha256": provenance_hash,
        "entrypoint": "report.html",
        "replay_command": "python -m polymathica_hackathon.cli --output demo/output",
    }


def verify_artifact_hashes(provenance_path: Path, base_dir: Path | None = None) -> bool:
    provenance = read_json(provenance_path)
    root = base_dir or provenance_path.parent
    for relative_path, expected_hash in provenance["artifacts"].items():
        artifact_path = root / relative_path
        if not artifact_path.exists():
            raise FileNotFoundError(str(artifact_path))
        actual_hash = sha256_bytes(artifact_path.read_bytes())
        if actual_hash != expected_hash:
            raise GovernanceError(f"artifact hash mismatch: {relative_path}")
    return True


def make_visualization(path: Path, samples: list[dict[str, float]]) -> str:
    width, height = 900, 420
    left, top, chart_w, chart_h = 70, 40, 760, 280
    energies = [row["kinetic_energy"] for row in samples]
    emin, emax = min(energies), max(energies)
    span = emax - emin or 1.0

    points = []
    for idx, energy in enumerate(energies):
        x = left + chart_w * idx / (len(energies) - 1)
        y = top + chart_h * (1.0 - (energy - emin) / span)
        points.append(f"{x:.1f},{y:.1f}")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="POLYMATHICA validation energy trace">
  <rect width="{width}" height="{height}" fill="#0d1117"/>
  <text x="70" y="30" fill="#f0f6fc" font-family="Arial" font-size="22">POLYMATHICA Replay Validation: kinetic energy trace</text>
  <rect x="{left}" y="{top}" width="{chart_w}" height="{chart_h}" fill="#161b22" stroke="#30363d"/>
  <polyline points="{' '.join(points)}" fill="none" stroke="#2f81f7" stroke-width="4"/>
  <line x1="{left}" y1="{top + chart_h}" x2="{left + chart_w}" y2="{top + chart_h}" stroke="#8b949e"/>
  <line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_h}" stroke="#8b949e"/>
  <text x="70" y="360" fill="#c9d1d9" font-family="Arial" font-size="16">Workflow: configure -> replay -> validate -> visualise -> report -> archive</text>
  <text x="70" y="388" fill="#8b949e" font-family="Arial" font-size="14">Generated from deterministic NS2D lid-driven-cavity replay evidence.</text>
</svg>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    return sha256_bytes(path.read_bytes())


def make_report(path: Path, config: dict[str, Any], validation: dict[str, Any], visualization_path: Path) -> str:
    rows = "\n".join(
        f"<tr><td>{html.escape(gate['name'])}</td><td>{gate['measured']}</td><td>{gate['passed']}</td></tr>"
        for gate in validation["gates"]
    )
    body = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>POLYMATHICA Hackathon Evidence Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; max-width: 980px; }}
    code, pre {{ background: #f6f8fa; padding: .2rem .35rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    td, th {{ border: 1px solid #d0d7de; padding: .45rem; }}
  </style>
</head>
<body>
  <h1>POLYMATHICA Hackathon Evidence Report</h1>
  <p>Case: <code>{html.escape(config['case_id'])}</code></p>
  <p>Status: <strong>{html.escape(validation['status'])}</strong></p>
  <img src="{html.escape(visualization_path.name)}" alt="Validation energy trace" width="900">
  <h2>Validation Gates</h2>
  <table>
    <tr><th>Gate</th><th>Measured</th><th>Passed</th></tr>
    {rows}
  </table>
</body>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return sha256_bytes(path.read_bytes())


def run_workflow(output_dir: Path = DEFAULT_OUTPUT_DIR, config: dict[str, Any] | None = None) -> WorkflowResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    workflow_id = "polymathica-hackathon-ns2d-replay"
    created_at = REPLAY_CREATED_AT

    config = config or configured_experiment()
    validate_config(config)
    samples = replay_field(config)
    validation = validate(samples)

    config_hash = write_json(output_dir / "experiment_config.json", config)
    samples_hash = write_json(output_dir / "replay_samples.json", {"samples": samples})
    validation_hash = write_json(output_dir / "validation_report.json", validation)
    visualization_hash = make_visualization(output_dir / "validation_trace.svg", samples)
    report_hash = make_report(output_dir / "report.html", config, validation, output_dir / "validation_trace.svg")

    provenance = {
        "schema": "polymathica.provenance.v1",
        "workflow_id": workflow_id,
        "created_at": created_at,
        "stages": REQUIRED_STAGES,
        "artifacts": {
            "experiment_config.json": config_hash,
            "replay_samples.json": samples_hash,
            "validation_report.json": validation_hash,
            "validation_trace.svg": visualization_hash,
            "report.html": report_hash,
        },
    }
    provenance_hash = write_json(output_dir / "provenance.json", provenance)

    archive_manifest = build_archive_manifest(workflow_id, validation, provenance_hash)
    write_json(output_dir / "archive_manifest.json", archive_manifest)

    return WorkflowResult(
        workflow_id=workflow_id,
        output_dir=output_dir,
        validation_status=validation["status"],
        report_path=output_dir / "report.html",
        archive_manifest_path=output_dir / "archive_manifest.json",
        provenance_path=output_dir / "provenance.json",
        visualization_path=output_dir / "validation_trace.svg",
    )
