"""Pressure-projection benchmark for a known periodic Helmholtz split.

This benchmark complements the Taylor-Green viscous-decay case. It is not a
general Poisson solver. It is a compact, auditable pressure-projection reference
case where the irrotational contaminant lies in a known first Fourier mode.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .workflow import sha256_bytes, write_json

DEFAULT_PROJECTION_DIR = Path("demo/projection")


@dataclass(frozen=True)
class ProjectionResult:
    output_dir: Path
    status: str
    divergence_before: float
    divergence_after: float
    projected_l2_error: float
    potential_l2_error: float
    energy_removed: float
    report_path: Path


def projection_config() -> dict[str, Any]:
    return {
        "benchmark_id": "PERIODIC-PRESSURE-PROJECTION-KNOWN-MODE",
        "purpose": "verify an incompressibility projection on a known Helmholtz split",
        "grid": {"n": 32, "domain": [0.0, 2.0 * math.pi]},
        "contaminant": {
            "potential": "alpha * (sin(x) + sin(y))",
            "alpha": 0.125,
            "gradient": ["alpha * cos(x)", "alpha * cos(y)"],
        },
        "validation": {
            "divergence_reduction_factor": 1.0e12,
            "projected_l2_tolerance": 1.0e-14,
            "potential_l2_tolerance": 1.0e-14,
            "minimum_energy_removed": 1.0e-3,
        },
    }


def base_velocity(n: int) -> tuple[list[list[float]], list[list[float]]]:
    u = []
    v = []
    for i in range(n):
        x = 2.0 * math.pi * i / n
        u_row = []
        v_row = []
        for j in range(n):
            y = 2.0 * math.pi * j / n
            u_row.append(math.sin(x) * math.cos(y))
            v_row.append(-math.cos(x) * math.sin(y))
        u.append(u_row)
        v.append(v_row)
    return u, v


def potential_field(n: int, alpha: float) -> list[list[float]]:
    return [
        [alpha * (math.sin(2.0 * math.pi * i / n) + math.sin(2.0 * math.pi * j / n)) for j in range(n)]
        for i in range(n)
    ]


def potential_gradient(n: int, alpha: float) -> tuple[list[list[float]], list[list[float]]]:
    gx = []
    gy = []
    for i in range(n):
        x = 2.0 * math.pi * i / n
        gx_row = []
        gy_row = []
        for j in range(n):
            y = 2.0 * math.pi * j / n
            gx_row.append(alpha * math.cos(x))
            gy_row.append(alpha * math.cos(y))
        gx.append(gx_row)
        gy.append(gy_row)
    return gx, gy


def add_fields(
    a: list[list[float]],
    b: list[list[float]],
) -> list[list[float]]:
    n = len(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]


def subtract_fields(
    a: list[list[float]],
    b: list[list[float]],
) -> list[list[float]]:
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]


def divergence(u: list[list[float]], v: list[list[float]], dx: float) -> list[list[float]]:
    n = len(u)
    out = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        im = (i - 1) % n
        ip = (i + 1) % n
        for j in range(n):
            jm = (j - 1) % n
            jp = (j + 1) % n
            out[i][j] = (u[ip][j] - u[im][j]) / (2.0 * dx) + (v[i][jp] - v[i][jm]) / (2.0 * dx)
    return out


def l2_scalar(field: list[list[float]]) -> float:
    n = len(field)
    return math.sqrt(sum(field[i][j] * field[i][j] for i in range(n) for j in range(n)) / (n * n))


def l2_vector(
    u: list[list[float]],
    v: list[list[float]],
    u_ref: list[list[float]],
    v_ref: list[list[float]],
) -> float:
    n = len(u)
    total = 0.0
    for i in range(n):
        for j in range(n):
            du = u[i][j] - u_ref[i][j]
            dv = v[i][j] - v_ref[i][j]
            total += du * du + dv * dv
    return math.sqrt(total / (n * n))


def kinetic_energy(u: list[list[float]], v: list[list[float]]) -> float:
    n = len(u)
    return sum(u[i][j] * u[i][j] + v[i][j] * v[i][j] for i in range(n) for j in range(n)) / (2.0 * n * n)


def recover_first_mode_potential(div: list[list[float]]) -> tuple[list[list[float]], float]:
    n = len(div)
    numerator = 0.0
    denominator = 0.0
    for i in range(n):
        x = 2.0 * math.pi * i / n
        for j in range(n):
            y = 2.0 * math.pi * j / n
            basis = math.sin(x) + math.sin(y)
            numerator += div[i][j] * basis
            denominator += basis * basis

    # Central differences see d(cos)/dx as sin(dx)/dx times the continuous mode.
    dx = (2.0 * math.pi) / n
    discrete_wave_number = math.sin(dx) / dx
    alpha = -numerator / (discrete_wave_number * denominator)
    return potential_field(n, alpha), alpha


def make_projection_svg(path: Path, before: float, after: float) -> str:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 360" role="img" aria-label="Pressure projection divergence reduction">
  <rect width="900" height="360" fill="#0d1117"/>
  <text x="70" y="48" fill="#f0f6fc" font-family="Arial" font-size="24">Pressure projection benchmark</text>
  <rect x="80" y="110" width="260" height="120" fill="#8b949e"/>
  <rect x="560" y="110" width="80" height="120" fill="#2f81f7"/>
  <text x="80" y="260" fill="#c9d1d9" font-family="Arial" font-size="16">Before divergence L2: {before:.3e}</text>
  <text x="560" y="260" fill="#c9d1d9" font-family="Arial" font-size="16">After: {after:.3e}</text>
  <text x="70" y="310" fill="#8b949e" font-family="Arial" font-size="14">Known-mode Helmholtz split: velocity = divergence-free field + grad(phi), then project grad(phi) out.</text>
</svg>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    return sha256_bytes(path.read_bytes())


def run_projection_benchmark(output_dir: Path = DEFAULT_PROJECTION_DIR) -> ProjectionResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    config = projection_config()
    n = int(config["grid"]["n"])
    alpha = float(config["contaminant"]["alpha"])
    dx = (2.0 * math.pi) / n

    u_ref, v_ref = base_velocity(n)
    gx, gy = potential_gradient(n, alpha)
    u_dirty = add_fields(u_ref, gx)
    v_dirty = add_fields(v_ref, gy)

    div_before_field = divergence(u_dirty, v_dirty, dx)
    phi_recovered, alpha_recovered = recover_first_mode_potential(div_before_field)
    gx_recovered, gy_recovered = potential_gradient(n, alpha_recovered)
    u_projected = subtract_fields(u_dirty, gx_recovered)
    v_projected = subtract_fields(v_dirty, gy_recovered)
    div_after_field = divergence(u_projected, v_projected, dx)

    phi_exact = potential_field(n, alpha)
    div_before = l2_scalar(div_before_field)
    div_after = l2_scalar(div_after_field)
    projected_l2_error = l2_vector(u_projected, v_projected, u_ref, v_ref)
    potential_l2_error = l2_scalar(subtract_fields(phi_recovered, phi_exact))
    energy_removed = kinetic_energy(u_dirty, v_dirty) - kinetic_energy(u_projected, v_projected)
    reduction = div_before / div_after if div_after > 0.0 else math.inf

    tolerances = config["validation"]
    status = (
        "passed"
        if reduction >= tolerances["divergence_reduction_factor"]
        and projected_l2_error <= tolerances["projected_l2_tolerance"]
        and potential_l2_error <= tolerances["potential_l2_tolerance"]
        and energy_removed >= tolerances["minimum_energy_removed"]
        else "failed"
    )

    metrics = {
        "divergence_before_l2": div_before,
        "divergence_after_l2": div_after,
        "divergence_reduction_factor": reduction,
        "projected_l2_error": projected_l2_error,
        "potential_l2_error": potential_l2_error,
        "energy_removed": energy_removed,
        "alpha_exact": alpha,
        "alpha_recovered": alpha_recovered,
    }
    write_json(output_dir / "projection_config.json", config)
    write_json(output_dir / "projection_validation.json", {"schema": "polymathica.projection.validation.v1", "status": status, "metrics": metrics, "tolerances": tolerances})
    visualization_hash = make_projection_svg(output_dir / "projection_trace.svg", div_before, div_after)
    report = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>POLYMATHICA Projection Benchmark</title></head>
<body>
  <h1>Pressure Projection Benchmark</h1>
  <p>Status: <strong>{status}</strong></p>
  <p>Divergence before L2: {div_before:.6e}</p>
  <p>Divergence after L2: {div_after:.6e}</p>
  <p>Projected-field L2 error: {projected_l2_error:.6e}</p>
  <p>Recovered potential L2 error: {potential_l2_error:.6e}</p>
  <img src="projection_trace.svg" alt="Pressure projection divergence reduction" width="900">
</body>
</html>
"""
    report_path = output_dir / "projection_report.html"
    report_path.write_text(report, encoding="utf-8")
    manifest = {
        "schema": "polymathica.projection.archive.v1",
        "benchmark_id": config["benchmark_id"],
        "status": status,
        "artifacts": {
            "projection_config.json": sha256_bytes((output_dir / "projection_config.json").read_bytes()),
            "projection_validation.json": sha256_bytes((output_dir / "projection_validation.json").read_bytes()),
            "projection_trace.svg": visualization_hash,
            "projection_report.html": sha256_bytes(report_path.read_bytes()),
        },
    }
    write_json(output_dir / "projection_manifest.json", manifest)
    return ProjectionResult(
        output_dir=output_dir,
        status=status,
        divergence_before=div_before,
        divergence_after=div_after,
        projected_l2_error=projected_l2_error,
        potential_l2_error=potential_l2_error,
        energy_removed=energy_removed,
        report_path=report_path,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the public pressure-projection benchmark.")
    parser.add_argument("--output", default=str(DEFAULT_PROJECTION_DIR), help="Directory for projection artifacts.")
    args = parser.parse_args()
    result = run_projection_benchmark(Path(args.output))
    print(f"Projection benchmark: {result.status}")
    print(f"Divergence before L2: {result.divergence_before:.6e}")
    print(f"Divergence after L2: {result.divergence_after:.6e}")
    print(f"Projected L2 error: {result.projected_l2_error:.6e}")
    print(f"Potential L2 error: {result.potential_l2_error:.6e}")
    print(f"Energy removed: {result.energy_removed:.6e}")
    print(f"Report: {result.report_path}")
    return 0 if result.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
