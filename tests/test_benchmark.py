import tempfile
import unittest
from pathlib import Path

from polymathica_hackathon.benchmark import (
    advance_diffusion,
    benchmark_config,
    convergence_study,
    divergence_l2,
    error_metrics,
    initial_field,
    kinetic_energy,
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
            self.assertLessEqual(
                result.energy_relative_error,
                benchmark_config()["validation"]["energy_relative_tolerance"],
            )
            self.assertLessEqual(
                result.max_divergence_l2,
                benchmark_config()["validation"]["divergence_l2_tolerance"],
            )
            self.assertGreaterEqual(
                result.observed_order,
                benchmark_config()["validation"]["minimum_observed_order"],
            )
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

    def test_initial_taylor_green_field_is_discrete_divergence_free(self) -> None:
        u, v = initial_field(32)

        self.assertLessEqual(divergence_l2(u, v, (2.0 * 3.141592653589793) / 32), 1.0e-12)

    def test_reference_energy_matches_known_initial_value(self) -> None:
        u, v = initial_field(32)

        self.assertAlmostEqual(kinetic_energy(u, v), 0.25, places=14)

    def test_error_metrics_detect_exact_match(self) -> None:
        u, v = initial_field(8)
        metrics = error_metrics(u, v, u, v)

        self.assertEqual(metrics["l2_error"], 0.0)
        self.assertEqual(metrics["max_error"], 0.0)

    def test_grid_convergence_is_second_order(self) -> None:
        study = convergence_study([16, 32, 64], nu=0.01, dt=0.001, steps=100)

        self.assertGreaterEqual(study["mean_observed_order"], 1.9)
        self.assertEqual([row["n"] for row in study["rows"]], [16, 32, 64])


if __name__ == "__main__":
    unittest.main()
