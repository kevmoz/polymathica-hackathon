import tempfile
import unittest
from pathlib import Path

from polymathica_hackathon.projection import (
    add_fields,
    base_velocity,
    divergence,
    l2_scalar,
    potential_gradient,
    projection_config,
    recover_first_mode_potential,
    run_projection_benchmark,
    subtract_fields,
)


class ProjectionTests(unittest.TestCase):
    def test_projection_benchmark_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_projection_benchmark(Path(tmp))

            self.assertEqual(result.status, "passed")
            self.assertLessEqual(result.projected_l2_error, projection_config()["validation"]["projected_l2_tolerance"])
            self.assertLessEqual(result.potential_l2_error, projection_config()["validation"]["potential_l2_tolerance"])
            self.assertGreater(result.energy_removed, projection_config()["validation"]["minimum_energy_removed"])
            self.assertTrue(result.report_path.exists())

    def test_projection_reduces_divergence_by_large_factor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_projection_benchmark(Path(tmp))

            self.assertGreaterEqual(
                result.divergence_before / result.divergence_after,
                projection_config()["validation"]["divergence_reduction_factor"],
            )

    def test_recovered_first_mode_potential_matches_known_alpha(self) -> None:
        n = 32
        alpha = projection_config()["contaminant"]["alpha"]
        dx = (2.0 * 3.141592653589793) / n
        u_ref, v_ref = base_velocity(n)
        gx, gy = potential_gradient(n, alpha)
        div = divergence(add_fields(u_ref, gx), add_fields(v_ref, gy), dx)
        _, alpha_recovered = recover_first_mode_potential(div)

        self.assertAlmostEqual(alpha_recovered, alpha, places=14)

    def test_projection_is_idempotent_on_projected_field(self) -> None:
        n = 32
        alpha = projection_config()["contaminant"]["alpha"]
        dx = (2.0 * 3.141592653589793) / n
        u_ref, v_ref = base_velocity(n)
        gx, gy = potential_gradient(n, alpha)
        div = divergence(add_fields(u_ref, gx), add_fields(v_ref, gy), dx)
        _, alpha_recovered = recover_first_mode_potential(div)
        gx_recovered, gy_recovered = potential_gradient(n, alpha_recovered)
        u_projected = subtract_fields(add_fields(u_ref, gx), gx_recovered)
        v_projected = subtract_fields(add_fields(v_ref, gy), gy_recovered)

        self.assertLessEqual(l2_scalar(divergence(u_projected, v_projected, dx)), 1.0e-12)


if __name__ == "__main__":
    unittest.main()
