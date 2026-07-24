# Reviewer Note

This repository is a public demonstration package for the broader POLYMATHICA ecosystem.

It is designed to be inspectable in minutes and reproducible on a standard Python installation. The goal is not to expose every private runtime component, but to show the operating pattern clearly:

```text
configured experiment -> governed execution -> validation gates -> visual evidence -> provenance -> archive manifest
```

## What Reviewers Can Verify Here

- runnable workflow execution
- deterministic validation reports
- negative-path governance tests
- artifact hashing and provenance records
- CI execution on GitHub Actions
- three compact numerical benchmark families
- analytic reference comparisons
- convergence evidence for Taylor-Green and Poiseuille cases
- public release media connected to the broader POLYMATHICA workspace

## Scope Boundary

This repository does not claim to be the complete POLYMATHICA platform, the full PSIC reasoning system, the complete Graphics Core, or the full Olana governance runtime.

It demonstrates selected capabilities in a compact public form so judges can verify the submission without needing access to the larger private development workspace.

## Why This Package Exists

Hackathon judges need a fast path from claim to evidence. This repository keeps that path short:

```bash
python -m pip install -e .
python -m polymathica_hackathon.cli --output demo/output
python -m polymathica_hackathon.benchmark --output demo/benchmark
python -m polymathica_hackathon.projection --output demo/projection
python -m polymathica_hackathon.poiseuille --output demo/poiseuille
python -m unittest discover -s tests
```

The broader POLYMATHICA vision matters, but this public package is intentionally judged on executable evidence.
