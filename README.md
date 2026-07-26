# POLYMATHICA Hackathon Demonstration

A governed scientific workflow that converts a configured Navier-Stokes experiment into validated, replayable and provenance-linked scientific evidence.

[![tests](https://github.com/kevmoz/polymathica-hackathon/actions/workflows/tests.yml/badge.svg)](https://github.com/kevmoz/polymathica-hackathon/actions/workflows/tests.yml)

## Judge Links

- GitHub Pages gallery: https://kevmoz.github.io/polymathica-hackathon
- Release videos: https://github.com/kevmoz/polymathica-hackathon/releases/tag/v1.0.0-hackathon
- Judging guide: [docs/JUDGING_GUIDE.md](docs/JUDGING_GUIDE.md)
- Reviewer note: [docs/REVIEWER_NOTE.md](docs/REVIEWER_NOTE.md)
- Scorecard response: [docs/SCORECARD_RESPONSE.md](docs/SCORECARD_RESPONSE.md)
- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- API reference: [docs/API_REFERENCE.md](docs/API_REFERENCE.md)
- Verification dossier: [docs/VERIFICATION.md](docs/VERIFICATION.md)
- Validation notes: [docs/VALIDATION.md](docs/VALIDATION.md)
- Public benchmark solver: [docs/BENCHMARK.md](docs/BENCHMARK.md)
- Benchmark matrix: [docs/BENCHMARK_MATRIX.md](docs/BENCHMARK_MATRIX.md)
- Pressure-projection benchmark: [docs/PROJECTION.md](docs/PROJECTION.md)
- Poiseuille channel benchmark: [docs/POISEUILLE.md](docs/POISEUILLE.md)
- July 25 progress showcase: [docs/PROGRESS_2026_07_25.md](docs/PROGRESS_2026_07_25.md)
- Video compression guide: [docs/VIDEO_COMPRESSION.md](docs/VIDEO_COMPRESSION.md)

## Demonstrated Workflow

```text
Create -> Configure -> Run or Replay -> Validate -> Visualise -> Report -> Archive
```

This repository is the compact public submission package for judges. It contains a runnable deterministic replay workflow, tests, CI configuration, generated evidence, documentation, and links to seven real simulation videos published as GitHub Release assets.

We are not asking you to trust our vision. This repository is a compact, runnable evidence package that demonstrates the operating pattern behind the broader POLYMATHICA ecosystem.

## Public Demo Scope

This repository demonstrates the governed evidence workflow using a deterministic Navier-Stokes replay.

It does not contain the complete private POLYMATHICA solver, PSIC, Graphics Core or Olana development repositories.

The public demo verifies orchestration, configuration governance, validation gates, scientific visualisation, report generation, provenance hashing, artifact integrity checks and archive creation. It also includes three compact benchmark families: Taylor-Green viscous decay, known-mode pressure projection and plane Poiseuille channel flow. The release videos show larger GPU/rendering outputs prepared from the broader POLYMATHICA workspace.

## July 25 Progress Update

The latest private-workspace evidence added for judges is the V533 CFD room showcase and a reproducible Taylor-Green vortex comparison pair.

- V533 operator-room video: [docs/assets/v533_cfd_room_showcase_silent.mp4](docs/assets/v533_cfd_room_showcase_silent.mp4)
- V533 still image: [docs/assets/v533_cfd_room_showcase_export.png](docs/assets/v533_cfd_room_showcase_export.png)
- Progress note: [docs/PROGRESS_2026_07_25.md](docs/PROGRESS_2026_07_25.md)
- Source comparison: `CMP-20260725-223914-d2742d`
- Source runs: `CFD-20260725-223859-a6e661` and `CFD-20260725-223906-62d046`

The source capture passed browser, manifest, PNG export, video validity and frame-linking checks. The Taylor-Green comparison was equivalent within tolerance with passed analytical validation in both source runs.

## Run In Three Commands

```bash
git clone https://github.com/kevmoz/polymathica-hackathon.git
cd polymathica-hackathon
python -m pip install -e .
python -m polymathica_hackathon.suite --output demo
python -m polymathica_hackathon.verify --root demo --report demo/verification_report.json
python -m unittest discover -s tests
```

Expanded component path:

```bash
python -m polymathica_hackathon.cli --output demo/output
python -m polymathica_hackathon.benchmark --output demo/benchmark
python -m polymathica_hackathon.projection --output demo/projection
python -m polymathica_hackathon.poiseuille --output demo/poiseuille
python -m unittest discover -s tests
```

No external runtime dependencies are required for the demo workflow.

No-install fallback:

```bash
PYTHONPATH=src python -m polymathica_hackathon.cli --output demo/output
```

## Evidence Included

- Source workflow: [src/polymathica_hackathon/workflow.py](src/polymathica_hackathon/workflow.py)
- Tests: [tests/test_workflow.py](tests/test_workflow.py)
- CI: [.github/workflows/tests.yml](.github/workflows/tests.yml)
- Generated config: [demo/output/experiment_config.json](demo/output/experiment_config.json)
- Validation report: [demo/output/validation_report.json](demo/output/validation_report.json)
- Provenance record: [demo/output/provenance.json](demo/output/provenance.json)
- Archive manifest: [demo/output/archive_manifest.json](demo/output/archive_manifest.json)
- HTML report: [demo/output/report.html](demo/output/report.html)
- Scientific visualisation: [demo/output/validation_trace.svg](demo/output/validation_trace.svg)
- Benchmark solver: [src/polymathica_hackathon/benchmark.py](src/polymathica_hackathon/benchmark.py)
- Benchmark validation: [demo/benchmark/benchmark_validation.json](demo/benchmark/benchmark_validation.json)
- Benchmark convergence study: [demo/benchmark/convergence_study.json](demo/benchmark/convergence_study.json)
- Benchmark report: [demo/benchmark/benchmark_report.html](demo/benchmark/benchmark_report.html)
- Projection validation: [demo/projection/projection_validation.json](demo/projection/projection_validation.json)
- Projection report: [demo/projection/projection_report.html](demo/projection/projection_report.html)
- Poiseuille validation: [demo/poiseuille/poiseuille_validation.json](demo/poiseuille/poiseuille_validation.json)
- Poiseuille convergence: [demo/poiseuille/poiseuille_convergence.json](demo/poiseuille/poiseuille_convergence.json)
- Poiseuille report: [demo/poiseuille/poiseuille_report.html](demo/poiseuille/poiseuille_report.html)
- Complete evidence suite summary: [demo/evidence_suite_summary.json](demo/evidence_suite_summary.json)
- Complete evidence suite manifest: [demo/evidence_suite_manifest.json](demo/evidence_suite_manifest.json)
- Verification report: [demo/verification_report.json](demo/verification_report.json)

Benchmark summary:

- Taylor-Green viscous-decay velocity benchmark
- analytic velocity-field and kinetic-energy references
- grid convergence at `n = 16, 32, 64`
- observed convergence order: `2.005`
- final velocity L2 error: `4.514621e-06`
- max divergence L2: `1.052400e-15`

Projection summary:

- known-mode periodic Helmholtz split
- pressure/potential component recovered from divergence
- divergence reduced from `1.241984e-01` to `6.678177e-16`
- projected-field L2 error: `5.770979e-17`

Poiseuille summary:

- pressure-driven steady Stokes channel-flow benchmark
- analytic parabolic velocity profile and reference values
- bulk flow-rate convergence at `n = 16, 32, 64, 128`
- centerline velocity reference: `1/8`
- bulk flow-rate reference: `1/12`
- wall-shear magnitude reference: `1/2`

## Core Systems

- POLYMATHICA: experiment orchestration, execution state, evidence lifecycle and institute interface.
- PSIC: scientific reasoning, planning, validation interpretation and research coordination.
- Graphics Core: scientific rendering, replay and media evidence generation.
- Olana: scientific oversight, contradiction analysis, governance review and experiment discussion.

## What Is Original Here

The submission focuses on the evidence pattern: every public claim is tied to a runnable workflow, generated artifacts, validation gates, provenance hashes, documentation, or release media. The hackathon repo is deliberately small so judges can inspect it quickly without needing the larger development workspace.

## Video Assets

The release contains seven prepared videos:

- `polymathica_60s_cinematic.mp4`
- `polymathica_ns_cinematic.mp4`
- `polymathica_graphics_core_postfx.mp4`
- `polymathica_ns_results.mp4`
- `polymathica_3d_gpu_cuda_60s.mp4`
- `polymathica_2d_validation_replay.mp4`
- `polymathica_lab_workflow.mp4`
- `docs/assets/v533_cfd_room_showcase_silent.mp4`

To refresh release assets from the local POLYMATHICA workspace:

```bash
python scripts/organize_videos.py --yes
python scripts/upload_release_assets.py
```

To prepare smaller balanced H.265/HEVC copies:

```bash
python scripts/organize_videos.py --yes --compress-hevc --hevc-crf 23 --hevc-preset slow
```

See [docs/VIDEO_MANIFEST.md](docs/VIDEO_MANIFEST.md) for source mappings and playback notes.
