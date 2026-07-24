# Scorecard Response

This repository directly addresses the most important judge-readiness concerns:

| Concern | Public Evidence |
| --- | --- |
| Empty flagship repository | README, source package, tests, docs, demo output and CI are present. |
| Claims without verification | Validation report, provenance hashes, archive manifest and report are committed. |
| Unclear run path | README and judging guide include direct run commands. |
| Replay vs live solver ambiguity | Public demo scope states this is a deterministic replay evidence workflow. |
| Weak governance proof | Tests cover invalid config rejection, archive blocking, missing artifacts and hash tampering. |
| System ownership ambiguity | README and architecture docs define POLYMATHICA, PSIC, Graphics Core and Olana roles. |
| Need benchmark-backed solver evidence | `src/polymathica_hackathon/benchmark.py` runs a Taylor-Green solver and compares against analytic velocity and energy references. |
| Need convergence proof | `demo/benchmark/convergence_study.json` records n = 16, 32, 64 convergence with observed order 2.005. |
| Need incompressibility evidence | `demo/benchmark/benchmark_validation.json` records max divergence L2 near machine precision. |
| Need pressure/projection context | `src/polymathica_hackathon/projection.py` runs a known-mode pressure-projection benchmark and commits validation artifacts. |
| Need multiple independent canonical checks | The public package now includes Taylor-Green viscous decay and a pressure-projection benchmark. |

The current public package is intentionally compact: it is designed to be inspectable in minutes, while the release videos and gallery show larger simulation and rendering outputs from the broader POLYMATHICA workspace.
