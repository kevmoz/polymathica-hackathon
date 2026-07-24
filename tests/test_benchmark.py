import tempfile
import unittest
from pathlib import Path

from polymathica_hackathon.benchmark import (
    advance_diffusion,
    benchmark_config,
    error_metrics,
    initial_field,
    reference_field,
    run_benchmark,
)


class BenchmarkTests(unittest.TestCase):
    def test_benchmark_solver_passes_reference_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_benchmark(Path(tmp))

            self.assertEqual(result.status, "passed")
            self.assertLessEqual(result.l2_error, benchmark_config()["validation"]["l2_tolerance"])
            self.assertLessEqual(result.max_error, benchmark_config()["validation"]["max_tolerance"])
            self.assertTrue(result.report_path.exists())
            self.assertTrue(result.visualization_path.exists())

    def test_reference_field_matches_initial_field_at_time_zero(self) -> None:
        u0, v0 = initial_field(16)
        u_ref, v_ref = reference_field(16, nu=0.01, t=0.0)

        self.assertEqual(u0, u_ref)
        self.assertEqual(v0, v_ref)

    def test_diffusion_step_reduces_energy(self) -> None:
        u, v = initial_field(16)
        before = sum(u[i][j] * u[i][j] + v[i][j] * v[i][j] for i in range(16) for j in range(16))
        u, v = advance_diffusion(u, v, nu=0.01, dt=0.001, steps=10, dx=(2.0 * 3.141592653589793) / 16)
        after = sum(u[i][j] * u[i][j] + v[i][j] * v[i][j] for i in range(16) for j in range(16))

        self.assertLess(after, before)

    def test_error_metrics_detect_exact_match(self) -> None:
        u, v = initial_field(8)
        metrics = error_metrics(u, v, u, v)

        self.assertEqual(metrics["l2_error"], 0.0)
        self.assertEqual(metrics["max_error"], 0.0)


if __name__ == "__main__":
    unittest.main()
