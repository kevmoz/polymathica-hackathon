# Architecture

POLYMATHICA is presented here as a compact judged workflow, not the full research workspace.

```text
Create
  -> Configure
  -> Run or Replay
  -> Validate
  -> Visualise
  -> Report
  -> Archive
```

## Systems

- POLYMATHICA: governed scientific workflow shell and evidence package.
- PSIC: physical simulation and instantiation context.
- Graphics Core: rendering and video export pathway.
- Olana: governance, validation, provenance and review logic.

## Demonstration Boundary

The hackathon repository includes one complete deterministic replay workflow in `src/polymathica_hackathon`. It is intentionally small, readable and testable, while the release assets and docs point to the larger local GPU-generated outputs.

![Architecture](assets/architecture.svg)
