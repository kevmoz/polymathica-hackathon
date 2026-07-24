# Benchmark Matrix

This page gives judges a one-screen map of the public numerical evidence.

| Benchmark | Canonical Role | Reference | Convergence / Metric | Public Artifacts |
| --- | --- | --- | --- | --- |
| Taylor-Green viscous decay | unsteady periodic vortex decay | analytic velocity field and kinetic-energy decay | velocity L2 grid convergence at `n = 16, 32, 64`; mean order `2.005`; max divergence near machine precision | `demo/benchmark/benchmark_validation.json`, `demo/benchmark/convergence_study.json` |
| Known-mode pressure projection | incompressibility correction on a controlled Helmholtz split | exact divergence-free velocity and exact irrotational potential | divergence reduced from `1.241984e-01` to `6.678177e-16`; projected-field L2 error `5.770979e-17` | `demo/projection/projection_validation.json`, `demo/projection/projection_manifest.json` |
| Plane Poiseuille channel flow | pressure-driven wall-bounded Stokes flow | analytic parabolic profile, centerline velocity `1/8`, bulk flow rate `1/12`, wall shear `1/2` | bulk flow-rate convergence at `n = 16, 32, 64, 128`; mean order `2.000` | `demo/poiseuille/poiseuille_validation.json`, `demo/poiseuille/poiseuille_convergence.json` |

## Reproduce All Numerical Evidence

```bash
python -m polymathica_hackathon.suite --output demo
```

Expanded component path:

```bash
python -m polymathica_hackathon.benchmark --output demo/benchmark
python -m polymathica_hackathon.projection --output demo/projection
python -m polymathica_hackathon.poiseuille --output demo/poiseuille
python -m unittest discover -s tests
```

## Scope Boundary

The public benchmark suite is intentionally compact and inspectable. It is designed to show reproducible numerical validation, honest scope boundaries and artifact-backed evidence for the hackathon submission.

It does not claim to expose the full private POLYMATHICA runtime or to replace a production CFD validation campaign.
