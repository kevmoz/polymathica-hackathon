import tempfile
import unittest
from pathlib import Path

from polymathica_hackathon.poiseuille import (
    analytic_velocity,
    convergence_study,
    poiseuille_config,
    run_poiseuille_benchmark,
    solve_poiseuille,
    trapezoid_integral,
)


class PoiseuilleTests(unittest.TestCase):
    def test_poiseuille_benchmark_passes_reference_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_poiseuille_benchmark(Path(tmp))

            self.assertEqual(result.status, "passed")
            self.assertLessEqual(result.l2_error, poiseuille_config()["validation"]["l2_tolerance"])
            self.assertLessEqual(result.max_error, poiseuille_config()["validation"]["max_tolerance"])
            self.assertLessEqual(result.flow_rate_error, poiseuille_config()["validation"]["flow_rate_tolerance"])
            self.assertLessEqual(result.wall_shear_error, poiseuille_config()["validation"]["wall_shear_tolerance"])
            self.assertGreaterEqual(result.observed_order, poiseuille_config()["validation"]["minimum_observed_order"])
            self.assertTrue(result.report_path.exists())
            self.assertTrue((Path(tmp) / "poiseuille_validation.json").exists())

    def test_analytic_reference_values_are_canonical(self) -> None:
        self.assertAlmostEqual(analytic_velocity(0.5, nu=1.0, forcing=1.0), 0.125)
        self.assertAlmostEqual(analytic_velocity(0.0, nu=1.0, forcing=1.0), 0.0)
        self.assertAlmostEqual(analytic_velocity(1.0, nu=1.0, forcing=1.0), 0.0)

    def test_solved_profile_matches_parabolic_reference(self) -> None:
        case = solve_poiseuille(32, nu=1.0, forcing=1.0)

        self.assertLessEqual(case["metrics"]["l2_error"], 1.0e-13)
        self.assertLessEqual(case["metrics"]["max_error"], 1.0e-13)
        self.assertAlmostEqual(case["metrics"]["centerline_velocity"], 0.125)

    def test_trapezoid_flow_rate_converges_second_order(self) -> None:
        study = convergence_study([16, 32, 64, 128], nu=1.0, forcing=1.0)

        self.assertGreaterEqual(study["mean_observed_order"], 1.95)
        self.assertEqual([row["n"] for row in study["rows"]], [16, 32, 64, 128])

    def test_flow_rate_reference_detects_quadrature_error(self) -> None:
        case = solve_poiseuille(16, nu=1.0, forcing=1.0)
        flow_rate = trapezoid_integral(case["y"], case["u"])

        self.assertLess(flow_rate, 1.0 / 12.0)
        self.assertGreater(1.0 / 12.0 - flow_rate, 0.0)


if __name__ == "__main__":
    unittest.main()
