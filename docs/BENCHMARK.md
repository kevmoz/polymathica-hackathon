# Public Benchmark Solver

This repository includes one small benchmark-backed solver example:

**Taylor-Green vortex viscous decay**

The solver uses:

- a 32x32 periodic grid
- explicit finite-difference viscous update
- analytic Taylor-Green reference field
- L2 and max-error comparison at final time
- independent analytic kinetic-energy decay comparison
- discrete divergence metric through the run
- grid-convergence study at n = 16, 32, 64
- committed validation, report, trace and archive artifacts

Current committed result:

| Metric | Value |
| --- | ---: |
| Final velocity L2 error | `4.514621e-06` |
| Final velocity max error | `6.384638e-06` |
| Energy relative error | `1.279488e-05` |
| Max divergence L2 | `1.052400e-15` |
| Mean observed grid-convergence order | `2.005` |

Run it:

```bash
python -m polymathica_hackathon.benchmark --output demo/benchmark
python -m unittest discover -s tests
```

Generated artifacts:

- `demo/benchmark/benchmark_config.json`
- `demo/benchmark/energy_history.json`
- `demo/benchmark/convergence_study.json`
- `demo/benchmark/benchmark_validation.json`
- `demo/benchmark/benchmark_trace.svg`
- `demo/benchmark/benchmark_report.html`
- `demo/benchmark/benchmark_manifest.json`

## Scope

This is not the full private POLYMATHICA solver stack. It is a public, modest-resolution benchmark designed to prove that the submission contains a real executable numerical solver path with a documented reference comparison.

## Equation Context

The public benchmark advances the viscous velocity-decay form:

```text
du/dt = nu * Laplacian(u)
dv/dt = nu * Laplacian(v)
```

For the classical Taylor-Green vortex, the nonlinear advection terms are balanced by the analytic pressure field, leaving this exponential velocity decay as a valid velocity benchmark. This benchmark therefore proves the public finite-difference viscous-decay path, reference comparison, divergence tracking and convergence behavior. It should not be read as a general-purpose complete Navier-Stokes solver.

![Benchmark trace](../demo/benchmark/benchmark_trace.svg)
