# POLYMATHICA Hackathon Demonstration

A governed scientific workflow that converts a configured Navier-Stokes experiment into validated, replayable and provenance-linked scientific evidence.

[![tests](https://github.com/kevmoz/polymathica-hackathon/actions/workflows/tests.yml/badge.svg)](https://github.com/kevmoz/polymathica-hackathon/actions/workflows/tests.yml)

## Judge Links

- GitHub Pages gallery: https://kevmoz.github.io/polymathica-hackathon
- Release videos: https://github.com/kevmoz/polymathica-hackathon/releases/tag/v1.0.0-hackathon
- Judging guide: [docs/JUDGING_GUIDE.md](docs/JUDGING_GUIDE.md)
- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Validation notes: [docs/VALIDATION.md](docs/VALIDATION.md)

## Demonstrated Workflow

```text
Create -> Configure -> Run or Replay -> Validate -> Visualise -> Report -> Archive
```

This repository is the compact public submission package for judges. It contains a runnable deterministic replay workflow, tests, CI configuration, generated evidence, documentation, and links to seven real simulation videos published as GitHub Release assets.

## Run In Three Commands

```bash
git clone https://github.com/kevmoz/polymathica-hackathon.git
cd polymathica-hackathon
python -m pip install -e .
python -m polymathica_hackathon.cli --output demo/output
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

## Core Systems

- POLYMATHICA: governed scientific workflow shell and evidence package.
- PSIC: physical simulation and instantiation context.
- Graphics Core: rendering and video export pathway.
- Olana: governance, validation, provenance and review logic.

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

To refresh release assets from the local POLYMATHICA workspace:

```bash
python scripts/organize_videos.py --yes
python scripts/upload_release_assets.py
```

See [docs/VIDEO_MANIFEST.md](docs/VIDEO_MANIFEST.md) for source mappings and playback notes.
