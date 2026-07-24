# Judging Guide

## Fast Path

1. Open the gallery: https://kevmoz.github.io/polymathica-hackathon
2. Review the release videos: https://github.com/kevmoz/polymathica-hackathon/releases/tag/v1.0.0-hackathon
3. Run the local evidence workflow:

```bash
git clone https://github.com/kevmoz/polymathica-hackathon.git
cd polymathica-hackathon
python -m pip install -e .
python -m polymathica_hackathon.cli --output demo/output
python -m polymathica_hackathon.benchmark --output demo/benchmark
python -m unittest discover -s tests
```

## What To Look For

- one complete workflow from configuration to archived evidence
- deterministic validation output
- provenance hashes tying artifacts together
- public gallery and release videos
- CI workflow for repeatable test execution
- negative-path tests that reject invalid configs, failed validation archives and tampered artifacts
- small public Taylor-Green benchmark solver with analytic reference comparison
- grid-convergence evidence showing observed second-order behavior
- divergence and analytic energy metrics for the benchmark

## Public Demo Scope

This repository demonstrates the governed evidence workflow using a deterministic Navier-Stokes replay. It does not contain the complete private POLYMATHICA solver, PSIC, Graphics Core or Olana repositories.

The public demo verifies orchestration, validation gates, visualisation, report generation, provenance, artifact hash checks and archive creation.

## Submission Claim

POLYMATHICA is a governed autonomous scientific laboratory pattern. This repository packages a judge-facing slice of that system with runnable evidence rather than only presentation material.
