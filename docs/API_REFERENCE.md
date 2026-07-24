# API Reference

This is the public API surface for the compact hackathon demonstration package.

The package intentionally exposes a small set of auditable functions and command-line entry points. It does not expose the complete private POLYMATHICA runtime.

## Command-Line Entry Points

| Command | Purpose | Main Artifacts |
| --- | --- | --- |
| `python -m polymathica_hackathon.suite --output demo` | Runs the full public evidence suite | `demo/evidence_suite_summary.json`, `demo/evidence_suite_manifest.json` |
| `python -m polymathica_hackathon.verify --root demo --report demo/verification_report.json` | Verifies manifest hashes and component statuses | `demo/verification_report.json` |
| `python -m polymathica_hackathon.cli --output demo/output` | Runs governed deterministic replay workflow | `validation_report.json`, `provenance.json`, `archive_manifest.json` |
| `python -m polymathica_hackathon.benchmark --output demo/benchmark` | Runs Taylor-Green viscous-decay benchmark | `benchmark_validation.json`, `convergence_study.json` |
| `python -m polymathica_hackathon.projection --output demo/projection` | Runs known-mode pressure-projection benchmark | `projection_validation.json`, `projection_manifest.json` |
| `python -m polymathica_hackathon.poiseuille --output demo/poiseuille` | Runs plane Poiseuille channel-flow benchmark | `poiseuille_validation.json`, `poiseuille_convergence.json` |

## `polymathica_hackathon.suite`

`run_evidence_suite(output_dir: Path = Path("demo")) -> EvidenceSuiteResult`

Runs the complete public package:

- governed replay workflow
- Taylor-Green benchmark
- pressure-projection benchmark
- Poiseuille benchmark
- artifact hash verification
- aggregate summary and manifest generation

`EvidenceSuiteResult` fields:

- `output_dir`
- `status`
- `workflow_status`
- `taylor_green_status`
- `projection_status`
- `poiseuille_status`
- `tests_expected`
- `summary_path`
- `manifest_path`

## `polymathica_hackathon.verify`

`verify_evidence_bundle(root: Path = Path("demo"), report_path: Path | None = None) -> VerificationResult`

Verifies the generated evidence suite by recomputing manifest hashes, checking component statuses and verifying workflow provenance hashes.

`VerificationResult` fields:

- `evidence_root`
- `status`
- `artifacts_checked`
- `components_checked`
- `report_path`

Important helpers:

- `verify_hashes(root: Path, manifest: dict) -> list[dict[str, str]]`
- `verify_component_statuses(root: Path, summary: dict) -> dict[str, str]`

## `polymathica_hackathon.workflow`

`run_workflow(output_dir: Path, config: dict | None = None) -> WorkflowResult`

Runs the governed replay workflow and writes validation, report, provenance and archive artifacts.

Important helpers:

- `configured_experiment() -> dict`
- `validate_config(config: dict) -> None`
- `replay_field(config: dict) -> list[dict[str, float]]`
- `validate(samples: list[dict[str, float]]) -> dict`
- `verify_artifact_hashes(provenance_path: Path, base_dir: Path | None = None) -> bool`

Public exceptions:

- `WorkflowConfigurationError`
- `GovernanceError`

## `polymathica_hackathon.benchmark`

`run_benchmark(output_dir: Path = Path("demo/benchmark")) -> BenchmarkResult`

Runs the Taylor-Green viscous-decay benchmark and writes analytic comparison, convergence, trace, report and manifest artifacts.

Important helpers:

- `benchmark_config() -> dict`
- `solve_case(n: int, nu: float, dt: float, steps: int) -> dict`
- `convergence_study(grid_sizes: list[int], nu: float, dt: float, steps: int) -> dict`

## `polymathica_hackathon.projection`

`run_projection_benchmark(output_dir: Path = Path("demo/projection")) -> ProjectionResult`

Runs the known-mode Helmholtz split benchmark and writes projection validation, trace, report and manifest artifacts.

Important helpers:

- `projection_config() -> dict`
- `base_velocity(n: int) -> tuple[list[list[float]], list[list[float]]]`
- `recover_first_mode_potential(div: list[list[float]]) -> tuple[list[list[float]], float]`

## `polymathica_hackathon.poiseuille`

`run_poiseuille_benchmark(output_dir: Path = Path("demo/poiseuille")) -> PoiseuilleResult`

Runs the steady plane Poiseuille channel-flow benchmark and writes profile, convergence, validation, trace, report and manifest artifacts.

Important helpers:

- `poiseuille_config() -> dict`
- `analytic_velocity(y: float, nu: float, forcing: float) -> float`
- `solve_poiseuille(n: int, nu: float, forcing: float) -> dict`
- `convergence_study(grid_sizes: list[int], nu: float, forcing: float) -> dict`

## Stability

The public API is intentionally small for the hackathon package. The JSON schema names in committed artifacts are versioned with `.v1` suffixes so reviewers can inspect compatibility boundaries directly.
