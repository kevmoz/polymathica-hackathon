"""Plane Poiseuille benchmark with analytic channel-flow reference values.

The case solves the steady pressure-driven Stokes balance

    nu * d2u/dy2 + forcing = 0

with no-slip walls at y = 0 and y = 1. The analytic velocity profile is
parabolic, which makes this a compact wall-bounded benchmark with exact
reference values for centerline velocity, bulk flow rate and wall shear.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .workflow import sha256_bytes, write_json

DEFAULT_POISEUILLE_DIR = Path("demo/poiseuille")


@dataclass(frozen=True)
class PoiseuilleResult:
    output_dir: Path
    status: str
    l2_error: float
    max_error: float
    flow_rate_error: float
    wall_shear_error: float
    observed_order: float
    report_path: Path


def poiseuille_config() -> dict[str, Any]:
    return {
        "benchmark_id": "PLANE-POISEUILLE-STEADY-STOKES",
        "equation_family": "steady incompressible Stokes channel flow",
        "public_scope": "canonical pressure-driven wall-bounded flow benchmark",
        "grid": {"n": 32, "domain": [0.0, 1.0]},
        "parameters": {"nu": 1.0, "forcing": 1.0},
        "reference": {
            "velocity": "u(y) = forcing * y * (1-y) / (2*nu)",
            "centerline_velocity": 0.125,
            "bulk_flow_rate": 1.0 / 12.0,
            "wall_shear_magnitude": 0.5,
        },
        "validation": {
            "l2_tolerance": 1.0e-13,
            "max_tolerance": 1.0e-13,
            "flow_rate_tolerance": 1.0e-4,
            "wall_shear_tolerance": 1.0e-12,
            "minimum_observed_order": 1.95,
        },
        "convergence": {"grid_sizes": [16, 32, 64, 128]},
    }


def analytic_velocity(y: float, *, nu: float, forcing: float) -> float:
    return forcing * y * (1.0 - y) / (2.0 * nu)


def solve_tridiagonal(lower: list[float], diag: list[float], upper: list[float], rhs: list[float]) -> list[float]:
    """Thomas algorithm for the small one-dimensional benchmark system."""

    n = len(diag)
    c_prime = [0.0 for _ in range(n)]
    d_prime = [0.0 for _ in range(n)]
    c_prime[0] = upper[0] / diag[0] if n > 1 else 0.0
    d_prime[0] = rhs[0] / diag[0]

    for i in range(1, n):
        denom = diag[i] - lower[i] * c_prime[i - 1]
        c_prime[i] = upper[i] / denom if i < n - 1 else 0.0
        d_prime[i] = (rhs[i] - lower[i] * d_prime[i - 1]) / denom

    x = [0.0 for _ in range(n)]
    x[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]
    return x


def solve_poiseuille(n: int, *, nu: float, forcing: float) -> dict[str, Any]:
    dy = 1.0 / n
    interior = n - 1
    lower = [0.0] + [-nu / (dy * dy) for _ in range(interior - 1)]
    diag = [2.0 * nu / (dy * dy) for _ in range(interior)]
    upper = [-nu / (dy * dy) for _ in range(interior - 1)] + [0.0]
    rhs = [forcing for _ in range(interior)]
    interior_u = solve_tridiagonal(lower, diag, upper, rhs)
    y = [j * dy for j in range(n + 1)]
    u = [0.0] + interior_u + [0.0]
    u_ref = [analytic_velocity(value, nu=nu, forcing=forcing) for value in y]
    metrics = poiseuille_metrics(y, u, u_ref, nu=nu, forcing=forcing)
    return {"n": n, "dy": dy, "y": y, "u": u, "u_ref": u_ref, "metrics": metrics}


def trapezoid_integral(y: list[float], values: list[float]) -> float:
    total = 0.0
    for left in range(len(y) - 1):
        total += 0.5 * (values[left] + values[left + 1]) * (y[left + 1] - y[left])
    return total


def poiseuille_metrics(
    y: list[float],
    u: list[float],
    u_ref: list[float],
    *,
    nu: float,
    forcing: float,
) -> dict[str, float]:
    total = 0.0
    max_error = 0.0
    for actual, expected in zip(u, u_ref):
        error = abs(actual - expected)
        total += error * error
        max_error = max(max_error, error)

    dy = y[1] - y[0]
    flow_rate = trapezoid_integral(y, u)
    expected_flow_rate = forcing / (12.0 * nu)
    left_wall_shear = nu * (-3.0 * u[0] + 4.0 * u[1] - u[2]) / (2.0 * dy)
    right_wall_shear = nu * (3.0 * u[-1] - 4.0 * u[-2] + u[-3]) / (2.0 * dy)
    expected_shear = forcing / 2.0

    return {
        "l2_error": math.sqrt(total / len(u)),
        "max_error": max_error,
        "centerline_velocity": max(u),
        "analytic_centerline_velocity": forcing / (8.0 * nu),
        "bulk_flow_rate": flow_rate,
        "analytic_bulk_flow_rate": expected_flow_rate,
        "flow_rate_error": abs(flow_rate - expected_flow_rate),
        "left_wall_shear": left_wall_shear,
        "right_wall_shear": right_wall_shear,
        "wall_shear_error": max(abs(abs(left_wall_shear) - expected_shear), abs(abs(right_wall_shear) - expected_shear)),
    }


def convergence_study(grid_sizes: list[int], *, nu: float, forcing: float) -> dict[str, Any]:
    rows = []
    for n in grid_sizes:
        case = solve_poiseuille(n, nu=nu, forcing=forcing)
        rows.append(
            {
                "n": n,
                "dy": case["dy"],
                "flow_rate_error": case["metrics"]["flow_rate_error"],
                "l2_error": case["metrics"]["l2_error"],
                "wall_shear_error": case["metrics"]["wall_shear_error"],
            }
        )

    orders = []
    for previous, current in zip(rows, rows[1:]):
        orders.append(math.log(previous["flow_rate_error"] / current["flow_rate_error"], 2.0))
    return {
        "schema": "polymathica.poiseuille.convergence.v1",
        "quantity": "bulk flow-rate error vs analytic Poiseuille reference",
        "rows": rows,
        "observed_orders": orders,
        "mean_observed_order": sum(orders) / len(orders),
    }


def make_poiseuille_svg(path: Path, y: list[float], u: list[float], u_ref: list[float]) -> str:
    width, height = 900, 420
    left, top, chart_w, chart_h = 90, 55, 710, 270
    umax = max(max(u), max(u_ref)) or 1.0

    def point(idx: int, values: list[float]) -> str:
        x = left + chart_w * values[idx] / umax
        plot_y = top + chart_h * (1.0 - y[idx])
        return f"{x:.1f},{plot_y:.1f}"

    numerical = " ".join(point(i, u) for i in range(len(y)))
    analytic = " ".join(point(i, u_ref) for i in range(len(y)))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="Poiseuille channel benchmark velocity profile">
  <rect width="{width}" height="{height}" fill="#0d1117"/>
  <text x="70" y="38" fill="#f0f6fc" font-family="Arial" font-size="22">Plane Poiseuille benchmark: parabolic channel profile</text>
  <rect x="{left}" y="{top}" width="{chart_w}" height="{chart_h}" fill="#161b22" stroke="#30363d"/>
  <line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_h}" stroke="#8b949e" stroke-width="2"/>
  <polyline points="{analytic}" fill="none" stroke="#f2cc60" stroke-width="7" opacity="0.75"/>
  <polyline points="{numerical}" fill="none" stroke="#2f81f7" stroke-width="3"/>
  <text x="70" y="360" fill="#c9d1d9" font-family="Arial" font-size="16">Numerical finite-difference Stokes solution overlaid on analytic parabolic profile.</text>
  <text x="70" y="388" fill="#8b949e" font-family="Arial" font-size="14">Reference values: centerline velocity 1/8, bulk flow rate 1/12, wall shear magnitude 1/2.</text>
</svg>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    return sha256_bytes(path.read_bytes())


def run_poiseuille_benchmark(output_dir: Path = DEFAULT_POISEUILLE_DIR) -> PoiseuilleResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    config = poiseuille_config()
    n = int(config["grid"]["n"])
    nu = float(config["parameters"]["nu"])
    forcing = float(config["parameters"]["forcing"])
    case = solve_poiseuille(n, nu=nu, forcing=forcing)
    metrics = case["metrics"]
    convergence = convergence_study(list(config["convergence"]["grid_sizes"]), nu=nu, forcing=forcing)
    tolerances = config["validation"]
    status = (
        "passed"
        if metrics["l2_error"] <= tolerances["l2_tolerance"]
        and metrics["max_error"] <= tolerances["max_tolerance"]
        and metrics["flow_rate_error"] <= tolerances["flow_rate_tolerance"]
        and metrics["wall_shear_error"] <= tolerances["wall_shear_tolerance"]
        and convergence["mean_observed_order"] >= tolerances["minimum_observed_order"]
        else "failed"
    )

    write_json(output_dir / "poiseuille_config.json", config)
    write_json(output_dir / "poiseuille_profile.json", {"schema": "polymathica.poiseuille.profile.v1", "y": case["y"], "u": case["u"], "u_ref": case["u_ref"]})
    write_json(output_dir / "poiseuille_convergence.json", convergence)
    validation = {
        "schema": "polymathica.poiseuille.validation.v1",
        "status": status,
        "metrics": metrics,
        "convergence": {
            "mean_observed_order": convergence["mean_observed_order"],
            "observed_orders": convergence["observed_orders"],
        },
        "reference": config["reference"],
        "tolerances": tolerances,
    }
    write_json(output_dir / "poiseuille_validation.json", validation)
    visualization_hash = make_poiseuille_svg(output_dir / "poiseuille_trace.svg", case["y"], case["u"], case["u_ref"])
    report = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>POLYMATHICA Poiseuille Benchmark</title></head>
<body>
  <h1>Plane Poiseuille Benchmark</h1>
  <p>Status: <strong>{status}</strong></p>
  <p>Velocity L2 error: {metrics['l2_error']:.6e}</p>
  <p>Velocity max error: {metrics['max_error']:.6e}</p>
  <p>Bulk flow-rate error: {metrics['flow_rate_error']:.6e}</p>
  <p>Wall-shear error: {metrics['wall_shear_error']:.6e}</p>
  <p>Mean observed flow-rate convergence order: {convergence['mean_observed_order']:.3f}</p>
  <img src="poiseuille_trace.svg" alt="Poiseuille benchmark velocity profile" width="900">
</body>
</html>
"""
    report_path = output_dir / "poiseuille_report.html"
    report_path.write_text(report, encoding="utf-8")
    manifest = {
        "schema": "polymathica.poiseuille.archive.v1",
        "benchmark_id": config["benchmark_id"],
        "status": status,
        "artifacts": {
            "poiseuille_config.json": sha256_bytes((output_dir / "poiseuille_config.json").read_bytes()),
            "poiseuille_profile.json": sha256_bytes((output_dir / "poiseuille_profile.json").read_bytes()),
            "poiseuille_convergence.json": sha256_bytes((output_dir / "poiseuille_convergence.json").read_bytes()),
            "poiseuille_validation.json": sha256_bytes((output_dir / "poiseuille_validation.json").read_bytes()),
            "poiseuille_trace.svg": visualization_hash,
            "poiseuille_report.html": sha256_bytes(report_path.read_bytes()),
        },
    }
    write_json(output_dir / "poiseuille_manifest.json", manifest)
    return PoiseuilleResult(
        output_dir=output_dir,
        status=status,
        l2_error=metrics["l2_error"],
        max_error=metrics["max_error"],
        flow_rate_error=metrics["flow_rate_error"],
        wall_shear_error=metrics["wall_shear_error"],
        observed_order=convergence["mean_observed_order"],
        report_path=report_path,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the public plane-Poiseuille benchmark.")
    parser.add_argument("--output", default=str(DEFAULT_POISEUILLE_DIR), help="Directory for Poiseuille artifacts.")
    args = parser.parse_args()
    result = run_poiseuille_benchmark(Path(args.output))
    print(f"Poiseuille benchmark: {result.status}")
    print(f"Velocity L2 error: {result.l2_error:.6e}")
    print(f"Velocity max error: {result.max_error:.6e}")
    print(f"Bulk flow-rate error: {result.flow_rate_error:.6e}")
    print(f"Wall-shear error: {result.wall_shear_error:.6e}")
    print(f"Mean observed order: {result.observed_order:.3f}")
    print(f"Report: {result.report_path}")
    return 0 if result.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
