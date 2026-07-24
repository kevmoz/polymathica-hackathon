"""Small public benchmark-backed solver example.

This is a deliberately modest Taylor-Green vortex viscous-decay benchmark. It
uses an explicit finite-difference periodic Laplacian and compares the final
velocity field with the analytic reference solution.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .workflow import sha256_bytes, write_json

DEFAULT_BENCHMARK_DIR = Path("demo/benchmark")


@dataclass(frozen=True)
class BenchmarkResult:
    output_dir: Path
    status: str
    l2_error: float
    max_error: float
    energy_relative_error: float
    max_divergence_l2: float
    observed_order: float
    report_path: Path
    visualization_path: Path


def benchmark_config() -> dict[str, Any]:
    return {
        "benchmark_id": "TAYLOR-GREEN-VORTEX-VISCOUS-DECAY",
        "equation_family": "incompressible Navier-Stokes",
        "public_scope": "small benchmark-backed solver example",
        "grid": {"n": 32, "domain": [0.0, 2.0 * math.pi]},
        "parameters": {"nu": 0.01, "dt": 0.001, "steps": 100},
        "reference": {
            "u": "sin(x) * cos(y) * exp(-2*nu*t)",
            "v": "-cos(x) * sin(y) * exp(-2*nu*t)",
        },
        "validation": {
            "l2_tolerance": 2.0e-4,
            "max_tolerance": 4.0e-4,
            "energy_relative_tolerance": 2.0e-4,
            "divergence_l2_tolerance": 1.0e-12,
            "minimum_observed_order": 1.9,
        },
        "convergence": {"grid_sizes": [16, 32, 64], "dt": 0.001, "steps": 100},
    }


def initial_field(n: int) -> tuple[list[list[float]], list[list[float]]]:
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


def laplacian(field: list[list[float]], dx: float) -> list[list[float]]:
    n = len(field)
    inv_dx2 = 1.0 / (dx * dx)
    out = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        im = (i - 1) % n
        ip = (i + 1) % n
        for j in range(n):
            jm = (j - 1) % n
            jp = (j + 1) % n
            out[i][j] = (field[ip][j] + field[im][j] + field[i][jp] + field[i][jm] - 4.0 * field[i][j]) * inv_dx2
    return out


def advance_diffusion(
    u: list[list[float]],
    v: list[list[float]],
    *,
    nu: float,
    dt: float,
    steps: int,
    dx: float,
) -> tuple[list[list[float]], list[list[float]]]:
    n = len(u)
    for _ in range(steps):
        lu = laplacian(u, dx)
        lv = laplacian(v, dx)
        for i in range(n):
            for j in range(n):
                u[i][j] += dt * nu * lu[i][j]
                v[i][j] += dt * nu * lv[i][j]
    return u, v


def reference_field(n: int, nu: float, t: float) -> tuple[list[list[float]], list[list[float]]]:
    decay = math.exp(-2.0 * nu * t)
    u, v = initial_field(n)
    for i in range(n):
        for j in range(n):
            u[i][j] *= decay
            v[i][j] *= decay
    return u, v


def error_metrics(
    u: list[list[float]],
    v: list[list[float]],
    u_ref: list[list[float]],
    v_ref: list[list[float]],
) -> dict[str, float]:
    n = len(u)
    total = 0.0
    max_error = 0.0
    for i in range(n):
        for j in range(n):
            du = u[i][j] - u_ref[i][j]
            dv = v[i][j] - v_ref[i][j]
            point_error = math.sqrt(du * du + dv * dv)
            total += point_error * point_error
            max_error = max(max_error, point_error)
    return {"l2_error": math.sqrt(total / (n * n)), "max_error": max_error}


def kinetic_energy(u: list[list[float]], v: list[list[float]]) -> float:
    n = len(u)
    return sum(u[i][j] * u[i][j] + v[i][j] * v[i][j] for i in range(n) for j in range(n)) / (2.0 * n * n)


def analytic_kinetic_energy(nu: float, t: float) -> float:
    return 0.25 * math.exp(-4.0 * nu * t)


def divergence_l2(u: list[list[float]], v: list[list[float]], dx: float) -> float:
    n = len(u)
    total = 0.0
    for i in range(n):
        im = (i - 1) % n
        ip = (i + 1) % n
        for j in range(n):
            jm = (j - 1) % n
            jp = (j + 1) % n
            div = (u[ip][j] - u[im][j]) / (2.0 * dx) + (v[i][jp] - v[i][jm]) / (2.0 * dx)
            total += div * div
    return math.sqrt(total / (n * n))


def solve_case(n: int, nu: float, dt: float, steps: int) -> dict[str, Any]:
    dx = (2.0 * math.pi) / n
    u, v = initial_field(n)
    history = []
    for step in range(steps + 1):
        t = step * dt
        energy = kinetic_energy(u, v)
        expected_energy = analytic_kinetic_energy(nu, t)
        history.append(
            {
                "step": step,
                "time": round(t, 6),
                "kinetic_energy": round(energy, 12),
                "analytic_kinetic_energy": round(expected_energy, 12),
                "energy_relative_error": abs(energy - expected_energy) / expected_energy,
                "divergence_l2": divergence_l2(u, v, dx),
            }
        )
        if step < steps:
            u, v = advance_diffusion(u, v, nu=nu, dt=dt, steps=1, dx=dx)

    u_ref, v_ref = reference_field(n, nu, steps * dt)
    metrics = error_metrics(u, v, u_ref, v_ref)
    final_energy = history[-1]["kinetic_energy"]
    expected_final_energy = history[-1]["analytic_kinetic_energy"]
    metrics["energy_relative_error"] = abs(final_energy - expected_final_energy) / expected_final_energy
    metrics["max_divergence_l2"] = max(row["divergence_l2"] for row in history)
    return {"n": n, "u": u, "v": v, "history": history, "metrics": metrics}


def convergence_study(grid_sizes: list[int], nu: float, dt: float, steps: int) -> dict[str, Any]:
    rows = []
    for n in grid_sizes:
        case = solve_case(n, nu, dt, steps)
        rows.append(
            {
                "n": n,
                "dx": (2.0 * math.pi) / n,
                "l2_error": case["metrics"]["l2_error"],
                "max_error": case["metrics"]["max_error"],
                "energy_relative_error": case["metrics"]["energy_relative_error"],
                "max_divergence_l2": case["metrics"]["max_divergence_l2"],
            }
        )

    orders = []
    for previous, current in zip(rows, rows[1:]):
        orders.append(math.log(previous["l2_error"] / current["l2_error"], 2.0))
    return {
        "schema": "polymathica.benchmark.convergence.v1",
        "quantity": "final velocity L2 error vs analytic Taylor-Green reference",
        "rows": rows,
        "observed_orders": orders,
        "mean_observed_order": sum(orders) / len(orders),
    }


def make_benchmark_svg(path: Path, history: list[dict[str, float]]) -> str:
    width, height = 900, 420
    left, top, chart_w, chart_h = 70, 55, 760, 250
    values = [row["kinetic_energy"] for row in history]
    vmin, vmax = min(values), max(values)
    span = vmax - vmin or 1.0
    points = []
    for idx, value in enumerate(values):
        x = left + chart_w * idx / (len(values) - 1)
        y = top + chart_h * (1.0 - (value - vmin) / span)
        points.append(f"{x:.1f},{y:.1f}")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="Taylor-Green benchmark energy decay">
  <rect width="{width}" height="{height}" fill="#0d1117"/>
  <text x="70" y="38" fill="#f0f6fc" font-family="Arial" font-size="22">Taylor-Green benchmark: viscous energy decay</text>
  <rect x="{left}" y="{top}" width="{chart_w}" height="{chart_h}" fill="#161b22" stroke="#30363d"/>
  <polyline points="{' '.join(points)}" fill="none" stroke="#2f81f7" stroke-width="4"/>
  <text x="70" y="350" fill="#c9d1d9" font-family="Arial" font-size="16">Finite-difference public solver compared against analytic reference.</text>
  <text x="70" y="378" fill="#8b949e" font-family="Arial" font-size="14">Resolution 32x32, periodic domain, explicit viscous update.</text>
</svg>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    return sha256_bytes(path.read_bytes())


def run_benchmark(output_dir: Path = DEFAULT_BENCHMARK_DIR) -> BenchmarkResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    config = benchmark_config()
    n = int(config["grid"]["n"])
    nu = float(config["parameters"]["nu"])
    dt = float(config["parameters"]["dt"])
    steps = int(config["parameters"]["steps"])
    dx = (2.0 * math.pi) / n

    case = solve_case(n, nu, dt, steps)
    history = case["history"]
    metrics = case["metrics"]
    convergence = convergence_study(
        list(config["convergence"]["grid_sizes"]),
        nu,
        float(config["convergence"]["dt"]),
        int(config["convergence"]["steps"]),
    )
    status = (
        "passed"
        if metrics["l2_error"] <= config["validation"]["l2_tolerance"]
        and metrics["max_error"] <= config["validation"]["max_tolerance"]
        and metrics["energy_relative_error"] <= config["validation"]["energy_relative_tolerance"]
        and metrics["max_divergence_l2"] <= config["validation"]["divergence_l2_tolerance"]
        and convergence["mean_observed_order"] >= config["validation"]["minimum_observed_order"]
        else "failed"
    )

    write_json(output_dir / "benchmark_config.json", config)
    write_json(output_dir / "energy_history.json", {"history": history})
    write_json(output_dir / "convergence_study.json", convergence)
    validation = {
        "schema": "polymathica.benchmark.validation.v1",
        "status": status,
        "metrics": metrics,
        "convergence": {
            "mean_observed_order": convergence["mean_observed_order"],
            "observed_orders": convergence["observed_orders"],
        },
        "reference": config["reference"],
        "tolerances": config["validation"],
    }
    write_json(output_dir / "benchmark_validation.json", validation)
    visualization_hash = make_benchmark_svg(output_dir / "benchmark_trace.svg", history)
    report = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>POLYMATHICA Taylor-Green Benchmark</title></head>
<body>
  <h1>Taylor-Green Vortex Benchmark</h1>
  <p>Status: <strong>{status}</strong></p>
  <p>L2 error: {metrics['l2_error']:.6e}</p>
  <p>Max error: {metrics['max_error']:.6e}</p>
  <p>Energy relative error: {metrics['energy_relative_error']:.6e}</p>
  <p>Max divergence L2: {metrics['max_divergence_l2']:.6e}</p>
  <p>Mean observed grid-convergence order: {convergence['mean_observed_order']:.3f}</p>
  <img src="benchmark_trace.svg" alt="Taylor-Green benchmark energy decay" width="900">
</body>
</html>
"""
    report_path = output_dir / "benchmark_report.html"
    report_path.write_text(report, encoding="utf-8")
    manifest = {
        "schema": "polymathica.benchmark.archive.v1",
        "benchmark_id": config["benchmark_id"],
        "status": status,
        "artifacts": {
            "benchmark_config.json": sha256_bytes((output_dir / "benchmark_config.json").read_bytes()),
            "convergence_study.json": sha256_bytes((output_dir / "convergence_study.json").read_bytes()),
            "energy_history.json": sha256_bytes((output_dir / "energy_history.json").read_bytes()),
            "benchmark_validation.json": sha256_bytes((output_dir / "benchmark_validation.json").read_bytes()),
            "benchmark_trace.svg": visualization_hash,
            "benchmark_report.html": sha256_bytes(report_path.read_bytes()),
        },
    }
    write_json(output_dir / "benchmark_manifest.json", manifest)
    return BenchmarkResult(
        output_dir=output_dir,
        status=status,
        l2_error=metrics["l2_error"],
        max_error=metrics["max_error"],
        energy_relative_error=metrics["energy_relative_error"],
        max_divergence_l2=metrics["max_divergence_l2"],
        observed_order=convergence["mean_observed_order"],
        report_path=report_path,
        visualization_path=output_dir / "benchmark_trace.svg",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the public Taylor-Green benchmark solver.")
    parser.add_argument("--output", default=str(DEFAULT_BENCHMARK_DIR), help="Directory for benchmark artifacts.")
    args = parser.parse_args()
    result = run_benchmark(Path(args.output))
    print(f"Benchmark: {result.status}")
    print(f"L2 error: {result.l2_error:.6e}")
    print(f"Max error: {result.max_error:.6e}")
    print(f"Energy relative error: {result.energy_relative_error:.6e}")
    print(f"Max divergence L2: {result.max_divergence_l2:.6e}")
    print(f"Mean observed order: {result.observed_order:.3f}")
    print(f"Report: {result.report_path}")
    return 0 if result.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
