# Judging Guide

## Fast Path

1. Open the gallery: https://kevmoz.github.io/polymathica-hackathon
2. Read the scope note: [REVIEWER_NOTE.md](REVIEWER_NOTE.md)
3. Review the release videos: https://github.com/kevmoz/polymathica-hackathon/releases/tag/v1.0.0-hackathon
4. Run the local evidence workflow:

```bash
git clone https://github.com/kevmoz/polymathica-hackathon.git
cd polymathica-hackathon
python -m pip install -e .
python -m polymathica_hackathon.suite --output demo
python -m polymathica_hackathon.verify --root demo --report demo/verification_report.json
python -m unittest discover -s tests
```

Optional expanded component path:

```bash
python -m polymathica_hackathon.cli --output demo/output
python -m polymathica_hackathon.benchmark --output demo/benchmark
python -m polymathica_hackathon.projection --output demo/projection
python -m polymathica_hackathon.poiseuille --output demo/poiseuille
python -m unittest discover -s tests
```

For the numerical evidence at a glance, open [BENCHMARK_MATRIX.md](BENCHMARK_MATRIX.md).

## What To Look For

- one complete workflow from configuration to archived evidence
- deterministic validation output
- provenance hashes tying artifacts together
- public gallery and release videos
- CI workflow for repeatable test execution
- API/reference documentation for public commands and callable functions
- independent verification command for evidence-suite hashes, statuses and provenance
- negative-path tests that reject invalid configs, failed validation archives and tampered artifacts
- small public Taylor-Green benchmark solver with analytic reference comparison
- grid-convergence evidence showing observed second-order behavior
- divergence and analytic energy metrics for the benchmark
- independent pressure-projection benchmark with a known Helmholtz split
- pressure-driven plane Poiseuille benchmark with analytic centerline, flow-rate and wall-shear references
- convergence evidence across multiple canonical quantities rather than a single visual output

## Public Demo Scope

This repository demonstrates the governed evidence workflow using a deterministic Navier-Stokes replay. It does not contain the complete private POLYMATHICA solver, PSIC, Graphics Core or Olana repositories.

The public demo verifies orchestration, validation gates, visualisation, report generation, provenance, artifact hash checks and archive creation. Its numerical evidence is intentionally compact but spans unsteady periodic decay, incompressibility projection and wall-bounded channel flow.

## Submission Claim

POLYMATHICA is a governed autonomous scientific laboratory pattern. This repository packages a judge-facing slice of that system with runnable evidence rather than only presentation material.
