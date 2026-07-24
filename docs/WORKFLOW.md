# POLYMATHICA Experiment Workflow

## Complete Experiment Lifecycle

### Phase 1: Research Question

**Input**: Natural language research question

```python
# Example
research_question = """
How does viscosity variation with temperature affect the stability of 
turbulent flow in a channel? I want to model a channel with Re=10000,
using the Navier-Stokes equations with temperature-dependent viscosity.
"""
```

**Process**: Olana processes the question and extracts:
- Domain description (channel geometry)
- Physics (N-S + heat transfer)
- Parameters (Re=10000)
- Boundary conditions
- Goals (stability analysis)

**Output**: Structured experiment definition

### Phase 2: Experiment Design

**PSIC Responsibilities**:
1. Propose computational approach
2. Suggest discretization scheme
3. Recommend solver parameters
4. Set up monitoring points
5. Define convergence criteria

**Dialogue with Olana**:
```
Olana: "For your temperature-dependent viscosity study, I recommend:
  - Finite difference discretization (staggered grid)
  - Domain: 4π×2×2 units (periodic in x)
  - Resolution: 256×128×128 (adaptive refinement in high-gradient zones)
  - Solver: Incompressible N-S with energy equation
  - Duration: 50 flow-through times
  - Monitoring: Kinetic energy, dissipation rate, temperature distribution"

User: "That sounds good. How long will the simulation take?"

Olana: "Estimated 2-3 hours on GPU. I'll monitor it and alert you if 
there are issues."
```

**Output**: Validated workflow configuration

### Phase 3: Configuration & Validation

**Configuration File** (`experiment.yaml`):
```yaml
experiment:
  name: "Temperature-Dependent Viscosity Stability Study"
  description: "Analysis of turbulent channel flow with temperature-dependent viscosity"
  
domain:
  type: channel
  length: 4π
  height: 2
  width: 2
  periodic_x: true
  
physics:
  equations: [navier_stokes, energy]
  properties:
    - name: viscosity
      type: temperature_dependent
      mu0: 0.001
      T_ref: 300
      beta: 0.008
    - name: thermal_conductivity
      type: temperature_dependent
      k0: 0.02
      beta: 0.0001
      
Discretization:
  method: finite_difference
  staggered_grid: true
  resolution: [256, 128, 128]
  adaptive_refinement:
    enabled: true
    gradient_threshold: 0.1
    
solver:
  type: incompressible_navier_stokes
  time_stepping: rk3
  dt_max: 0.001
  cfl_number: 0.4
  
validation:
  mass_conservation_tolerance: 1e-10
  energy_conservation_tolerance: 1e-8
  stability_check_interval: 10
  
monitoring:
  - variable: kinetic_energy
    interval: 100
  - variable: dissipation_rate
    interval: 100
  - variable: temperature_field
    interval: 500
  - variable: pressure_field
    interval: 500
```

**Validation Process**:
- ✓ Check parameter ranges
- ✓ Verify domain is sensible
- ✓ Confirm resolution is adequate
- ✓ Validate boundary conditions
- ✓ Check computational resources
- ✓ Estimate runtime and storage

**Output**: Validated, executable configuration

### Phase 4: Mesh Generation

**Process**:
```python
# Auto-generated from configuration
mesh = generate_mesh(
    domain=channel_domain,
    resolution=[256, 128, 128],
    adaptive_refinement=adaptive_config
)

print(f"Mesh created:")
print(f"  Total points: {mesh.n_points:,}")
print(f"  Min spacing: {mesh.min_spacing:.6f}")
print(f"  Max spacing: {mesh.max_spacing:.6f}")
print(f"  Aspect ratio: {mesh.aspect_ratio:.2f}")
print(f"  Memory: {mesh.memory_usage_gb:.2f} GB")
```

**Quality Checks**:
- ✓ No inverted elements
- ✓ Aspect ratios within bounds
- ✓ Smooth transitions
- ✓ Boundary layer resolution adequate

**Output**: Computational mesh with metadata

### Phase 5: Simulation Setup

**Initialization**:
```python
# Restart from previous run (checkpoint)
if checkpoint_exists:
    simulation = load_checkpoint(checkpoint_path)
else:
    # Initialize from scratch
    simulation = initialize_simulation(
        mesh=mesh,
        physics=physics_config,
        initial_conditions=ic_config
    )
```

**Initial Conditions**:
- Velocity field: Channel flow with turbulent fluctuations
- Temperature field: Constant (300K) with small perturbations
- Pressure: Computed from velocity field

**Output**: Ready-to-run simulation state

### Phase 6: Execution & Monitoring

**Real-time Monitoring**:
```
Time: 0.000s / 50.00s (0.0%)
  CFL: 0.38 | dt: 0.0008s
  KE: 0.245 | Dissipation: 0.018
  T_min: 298.2K | T_max: 301.8K
  Residual: 2.3e-7 | Convergence: OK
  Status: RUNNING (2.3 hrs remaining)

[████░░░░░░░░░░░░░░░░░░░░░░░░░░] 15%
```

**Monitoring Points**:
- Wall-clock time vs simulation time
- CFL number and timestep size
- Kinetic energy evolution
- Energy dissipation rate
- Temperature extrema and distribution
- Solver convergence
- GPU utilization
- Memory usage

**Output**: Continuous telemetry and progress reports

### Phase 7: Results Visualization

**Real-time Visualization**:
- Velocity field visualization (every 500 timesteps)
- Temperature field heatmap
- Streamlines and vorticity
- Kinetic energy time series
- Monitoring point probes

**Output**: Graphics files and interactive plots

### Phase 8: Evidence Recording

**Data Stored**:
```
research_archive/experiments/temp_dep_visc_001/
├── metadata.json
│   ├── created: 2026-07-24T10:30:00Z
│   ├── duration: 2h 45m 32s
│   ├── configuration_hash: abc123def456
│   └── researcher: kevmoz
├── configuration.yaml
├── mesh.h5
├── snapshots/
│   ├── snapshot_00000.h5
│   ├── snapshot_00100.h5
│   └── snapshot_final.h5
├── time_series/
│   ├── kinetic_energy.csv
│   ├── dissipation_rate.csv
│   └── temperature_extrema.csv
├── logs/
│   ├── solver.log
│   ├── performance.log
│   └── events.log
└── plots/
    ├── ke_evolution.png
    ├── final_velocity.png
    └── final_temperature.png
```

**Output**: Complete experiment record in archive

### Phase 9: Replay & Validation

**Reproduce Results**:
```python
# Load saved configuration and data
experiment = load_experiment("temp_dep_visc_001")

# Verify:
print(f"Configuration verified: {experiment.verify_configuration()}")
print(f"Data integrity: {experiment.verify_data()}")
print(f"Reproducibility: {experiment.test_reproducibility()}")

# Re-run subset if needed
replay_result = experiment.replay(start_time=25.0, end_time=50.0)
print(f"Replay validation: {'PASS' if replay_result.matches else 'FAIL'}")
```

**Output**: Validated evidence

### Phase 10: Analysis & Reporting

**Generate Report**:
```python
report = experiment.generate_report(
    include_figures=True,
    include_analysis=True,
    include_code=True,
    format='markdown'
)

print(report)
# Saves to: research_archive/experiments/temp_dep_visc_001/REPORT.md
```

**Report Contents**:
- Executive summary
- Research question and methodology
- Simulation parameters
- Key findings and plots
- Convergence analysis
- Comparison with literature
- Discussion and conclusions
- Code and configuration for reproducibility

**Output**: Publication-ready report

### Phase 11: Discussion with Olana

```
User: "What do these results tell us about temperature-dependent viscosity?"

Olana: "The simulation reveals three key insights:

1. Viscosity Stratification: The temperature-dependent viscosity creates
   three distinct zones with different viscosity profiles, affecting 
   momentum transfer.

2. Kinetic Energy: The kinetic energy decreases 12% compared to the 
   constant-viscosity case, suggesting temperature variations dissipate
   turbulent kinetic energy more efficiently.

3. Heat Transfer: The temperature distribution shows enhanced cooling
   near walls (15-20% faster than expected from constant-property model),
   validating the variable-property coupling.

These findings suggest that..."

User: "Can we test with a different temperature gradient?"

Olana: "Yes. Should I run a parametric study with gradients from 5K 
to 50K? That would take about 8 hours total."
```

**Output**: Dialogue-driven analysis and next experiments

### Phase 12: Archive & Publication

**Archival**:
- Evidence tagged with keywords
- Linked to related experiments
- Full provenance recorded
- Backed up to long-term storage

**Publication**:
```bash
# Export for publication
polymathica export --experiment temp_dep_visc_001 \
                   --format paper \
                   --output paper.pdf
```

**Output**: Published evidence and findings

## Error Handling & Recovery

### Common Issues

**Divergence**:
- Automatically checkpoint and reduce timestep
- Retry with smaller CFL number
- Alert researcher
- Continue if recoverable

**Out of Memory**:
- Switch to adaptive mesh refinement
- Reduce checkpoint frequency
- Use out-of-core computation if supported

**Convergence Failure**:
- Try alternative solver
- Refine mesh locally
- Adjust solver parameters
- Request researcher guidance

**Corrupted Data**:
- Recover from last valid checkpoint
- Alert researcher
- Continue from recovery point

## Performance Targets

| Task | Target | Typical Result |
|------|--------|----------------|
| Mesh generation | <5 min | 2-3 min |
| Validation | <1 min | 30 sec |
| Initialization | <5 min | 1-2 min |
| Time-stepping (per step) | <1 sec | 0.5-0.8 sec |
| Visualization (per snapshot) | <10 sec | 5-8 sec |
| Analysis/reporting | <5 min | 2-3 min |

## Workflow Integration

The complete workflow is implemented as a directed graph of tasks:

```
research_question → design → configure → validate → mesh → setup → 
run → monitor → visualize → record → replay_validate → analyze → 
discuss → archive → publish
```

Each task:
- Has clear inputs and outputs
- Performs validation
- Reports progress
- Handles errors
- Updates telemetry

**The workflow is never complete until the final step is done.**
