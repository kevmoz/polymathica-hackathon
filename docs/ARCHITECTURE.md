# POLYMATHICA System Architecture

## Overview

POLYMATHICA is built as a layered, modular system with four core components that work together to create a complete autonomous scientific laboratory.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│              POLYMATHICA LABORATORY                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │  OLANA - Conversational Scientific Agent   │   │
│  │  ├─ Natural language interface             │   │
│  │  ├─ Persistent dialogue context            │   │
│  │  ├─ Experiment guidance and discussion     │   │
│  │  └─ Learning from past experiments         │   │
│  └────────────────────────────────────────────┘   │
│                      ↓                              │
│  ┌────────────────────────────────────────────┐   │
│  │  PSIC - Polymath Scientific Intelligence   │   │
│  │  ├─ Experiment planning and reasoning      │   │
│  │  ├─ Workflow orchestration                 │   │
│  │  ├─ Validation and governance              │   │
│  │  └─ Research memory and evidence tracking  │   │
│  └────────────────────────────────────────────┘   │
│                      ↓                              │
│  ┌────────────────────────────────────────────┐   │
│  │  Computational Core                        │   │
│  │  ├─ Simulation engines (JAX/NumPy)         │   │
│  │  ├─ PDE solvers                            │   │
│  │  ├─ CFD pipelines                          │   │
│  │  └─ GPU-accelerated compute                │   │
│  └────────────────────────────────────────────┘   │
│                      ↓                              │
│  ┌────────────────────────────────────────────┐   │
│  │  Graphics Core                             │   │
│  │  ├─ Scientific rendering                   │   │
│  │  ├─ Real-time instrumentation              │   │
│  │  ├─ Evidence visualization                 │   │
│  │  └─ Publication-grade graphics             │   │
│  └────────────────────────────────────────────┘   │
│                      ↓                              │
│  ┌────────────────────────────────────────────┐   │
│  │  Research Archive                          │   │
│  │  ├─ Experiment records                     │   │
│  │  ├─ Validated evidence                     │   │
│  │  ├─ Publication repository                 │   │
│  │  └─ Historical context                     │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Core Components

### 1. OLANA - Conversational Scientific Agent

**Purpose**: Natural language interface to the laboratory

**Responsibilities**:
- Accept research questions and hypotheses in natural language
- Maintain persistent conversation context across sessions
- Provide guidance on experiment design
- Discuss results and suggest refinements
- Learn from past experimental outcomes

**Key Files**:
```
src/olana/
├── agent/
│   ├── __init__.py
│   ├── core.py          # Main agent logic
│   └── prompts.py       # System and role prompts
├── dialogue/
│   ├── __init__.py
│   ├── context.py       # Conversation context management
│   ├── memory.py        # Persistent dialogue memory
│   └── handlers.py      # Response generation
└── context/
    ├── __init__.py
    └── laboratory.py    # Laboratory state and context
```

### 2. PSIC - Polymath Scientific Intelligence Core

**Purpose**: Orchestration, reasoning, and governance engine

**Responsibilities**:
- Plan experimental workflows from natural language descriptions
- Reason about scientific methodology and design
- Validate experimental setup against governance standards
- Track and validate evidence quality
- Maintain research memory and learning systems
- Orchestrate simulation and visualization pipelines

**Key Files**:
```
src/psic/
├── core/
│   ├── __init__.py
│   ├── engine.py        # Main orchestration engine
│   └── workflow.py      # Workflow execution logic
├── reasoning/
│   ├── __init__.py
│   ├── planner.py       # Experiment planning
│   ├── validator.py     # Methodology validation
│   └── analyzer.py      # Results analysis
├── validation/
│   ├── __init__.py
│   ├── governance.py    # Governance rules
│   ├── evidence.py      # Evidence validation
│   └── metrics.py       # Quality metrics
└── memory/
    ├── __init__.py
    ├── store.py         # Memory storage
    ├── retrieval.py     # Memory retrieval
    └── learning.py      # Experiential learning
```

### 3. Graphics Core

**Purpose**: Visualization and instrumentation

**Responsibilities**:
- Render scientific simulations in real-time
- Create interactive instrumentation dashboards
- Generate publication-quality visualizations
- Record and replay simulation evidence
- Handle multi-dimensional data visualization

**Key Files**:
```
src/graphics_core/
├── rendering/
│   ├── __init__.py
│   ├── engine.py        # Rendering pipeline
│   ├── shaders.py       # GPU shader programs
│   └── buffers.py       # GPU buffer management
├── instrumentation/
│   ├── __init__.py
│   ├── dashboard.py     # Live monitoring
│   ├── gauges.py        # Scientific gauges
│   └── overlays.py      # Real-time overlays
└── visualization/
    ├── __init__.py
    ├── plots.py         # Static plots
    ├── animations.py    # Animation generation
    └── export.py        # Export formats
```

### 4. Computational Core

**Purpose**: Simulation and numerical computation

**Responsibilities**:
- Execute scientific simulations
- Solve differential equations
- Manage GPU-accelerated computation
- Handle numerical validation
- Provide performance profiling

**Key Files**:
```
src/experiments/
├── templates/
│   ├── __init__.py
│   ├── base_template.py      # Base experiment template
│   ├── fluid_dynamics.py      # CFD template
│   ├── pde_solver.py          # PDE template
│   └── physics_informed.py    # Physics-informed ML template
└── workflows/
    ├── __init__.py
    ├── simulation_workflow.py  # Standard simulation flow
    ├── validation_workflow.py  # Validation flow
    └── publication_workflow.py # Publication flow
```

## Data Flow

### Experiment Lifecycle

```
1. HYPOTHESIS (Natural Language)
   ↓ (Olana)
2. DIALOGUE & REFINEMENT
   ↓ (PSIC Planning)
3. EXPERIMENT DESIGN
   ↓ (PSIC Validation)
4. VALIDATED WORKFLOW
   ↓ (Computational Core)
5. SIMULATION EXECUTION
   ↓ (Graphics Core)
6. REAL-TIME VISUALIZATION
   ↓ (PSIC Analysis)
7. EVIDENCE VALIDATION
   ↓ (Research Archive)
8. RECORDED EVIDENCE
   ↓ (Olana Discussion)
9. RESULTS & NEW HYPOTHESES
```

## Integration Points

### Olana ↔ PSIC
- Natural language commands → Structured experiment definitions
- Results discussion ← Numerical analysis
- Guidance requests → Workflow recommendations

### PSIC ↔ Computational Core
- Validated workflows → Simulation parameters
- Execution status ← Progress reports
- Results ← Numerical outputs

### Computational Core ↔ Graphics Core
- Simulation state → Rendering data
- Frame requests ← Visualization output
- Performance metrics ↔ Instrumentation data

### Graphics Core ↔ Research Archive
- Visualization outputs → Evidence records
- Historical data ← Archive retrieval

## Governance Model

All experiments must pass through:

1. **Design Validation**: Is the methodology sound?
2. **Parameter Validation**: Are inputs within acceptable ranges?
3. **Execution Monitoring**: Is computation proceeding normally?
4. **Evidence Validation**: Does output meet quality standards?
5. **Archive Recording**: Is evidence properly documented?

No experiment bypasses this pipeline.

## Scalability Considerations

- **Horizontal**: Multiple simulation jobs via job queue
- **Vertical**: GPU utilization and batch processing
- **Storage**: Archive with compression and indexing
- **Distribution**: FastAPI for microservice decomposition

## API Surface

See [API_SPECIFICATION.md](API_SPECIFICATION.md) for complete API documentation.
