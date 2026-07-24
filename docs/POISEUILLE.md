# Plane Poiseuille Benchmark

This benchmark adds a canonical wall-bounded flow case to the public validation package.

It solves the steady pressure-driven Stokes balance

```text
nu * d2u/dy2 + forcing = 0
```

on `y in [0, 1]` with no-slip walls at `y = 0` and `y = 1`.

For `nu = 1` and `forcing = 1`, the analytic profile is:

```text
u(y) = y * (1 - y) / 2
```

Reference values:

- centerline velocity: `1/8`
- bulk flow rate: `1/12`
- wall-shear magnitude: `1/2`

## What This Proves

The case verifies that the public package can run and validate a pressure-driven wall-bounded benchmark against closed-form reference quantities.

It complements:

- Taylor-Green viscous decay, which checks unsteady periodic velocity and energy decay.
- Known-mode pressure projection, which checks incompressibility correction on a controlled Helmholtz split.

## What This Does Not Prove

This is a steady Stokes channel-flow benchmark, not a full turbulent channel-flow simulation and not a claim of production CFD performance.

The solver is intentionally pure Python and inspectable so judges can audit every numerical step.

## Reproduce

```bash
python -m polymathica_hackathon.poiseuille --output demo/poiseuille
```

Generated artifacts:

- `demo/poiseuille/poiseuille_config.json`
- `demo/poiseuille/poiseuille_profile.json`
- `demo/poiseuille/poiseuille_convergence.json`
- `demo/poiseuille/poiseuille_validation.json`
- `demo/poiseuille/poiseuille_trace.svg`
- `demo/poiseuille/poiseuille_report.html`
- `demo/poiseuille/poiseuille_manifest.json`

## Acceptance Criteria

The run passes when:

- velocity-field L2 error is below tolerance
- max velocity error is below tolerance
- bulk flow-rate error is below tolerance
- wall-shear error is below tolerance
- observed flow-rate convergence order is at least second order within tolerance

This gives the submission a third independent benchmark family with analytic reference values and committed reproducibility artifacts.
