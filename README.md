# POLYMATHICA — Governed Autonomous Scientific Laboratory

> From experiment to evidence. From evidence to discovery.

## System Vision

POLYMATHICA is a governed autonomous scientific intelligence laboratory designed to move from a research question to validated evidence through a reproducible computational workflow. It combines computational physics, scientific software, autonomous agents, and rigorous evidence governance into a single, production-grade system.

## Core Architecture

```
Hypothesis
    ↓
Experiment Design (Olana + PSIC)
    ↓
Simulation (Graphics Core + JAX/NumPy)
    ↓
Validation and Governance (PSIC)
    ↓
Scientific Visualisation (Graphics Core)
    ↓
Evidence, Memory and Learning (Research Archive)
    ↓
New Hypothesis
```

## Core Systems

| System | Purpose | Status |
|--------|---------|--------|
| **POLYMATHICA** | Autonomous scientific institute and end-to-end experiment environment | Active |
| **PSIC** | Polymath Scientific Intelligence Core for planning, reasoning, validation and research memory | Development |
| **Graphics Core** | Scientific rendering, instrumentation, replay, evidence visualisation and publication graphics | Development |
| **Olana** | Conversational scientific agent for experiment discussion, guidance and persistent laboratory context | Development |

## Engineering Standards

```
✓ NO PLACEHOLDERS
✓ NO MOCKUPS
✓ NO FAKE TELEMETRY
✓ NO CLAIMING COMPLETE WITHOUT WORKING OUTPUT
```

A laboratory workflow is only operational when it supports:
**Create → Configure → Mesh → Validate → Run → Monitor → Visualise → Record → Replay → Report → Discuss → Archive → Publish**

## Repository Structure

```
polymathica-hackathon/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ENGINEERING_STANDARDS.md
│   ├── WORKFLOW.md
│   └── API_SPECIFICATION.md
├── src/
│   ├── psic/
│   │   ├── core/
│   │   ├── reasoning/
│   │   ├── validation/
│   │   └── memory/
│   ├── graphics_core/
│   │   ├── rendering/
│   │   ├── instrumentation/
│   │   └── visualization/
│   ├── olana/
│   │   ├── agent/
│   │   ├── dialogue/
│   │   └── context/
│   └── experiments/
│       ├── templates/
│       └── workflows/
├── research_archive/
│   ├── experiments/
│   ├── evidence/
│   └── publications/
├── assets/
│   ├── video/
│   ├── diagrams/
│   └── media/
└── config/
    ├── governance/
    └── system/
```

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone https://github.com/kevmoz/polymathica-hackathon
   cd polymathica-hackathon
   python -m venv venv
   source venv/bin/activate  # or `venv\\Scripts\\activate` on Windows
   pip install -r requirements.txt
   ```

2. **Review Architecture**
   ```bash
   cat docs/ARCHITECTURE.md
   cat docs/ENGINEERING_STANDARDS.md
   ```

3. **Start with a Workflow Template**
   ```bash
   python src/experiments/templates/fluid_dynamics_template.py
   ```

## Technology Stack

- **Computational Core**: Python 3.10+, JAX, NumPy, SciPy
- **API Framework**: FastAPI, Pydantic
- **Frontend**: JavaScript, HTML5, CSS3
- **Visualization**: Matplotlib, Plotly, WebGL
- **GPU Computing**: NVIDIA CUDA
- **Infrastructure**: Docker, GitHub Actions
- **Version Control**: Git, GitHub

## Research Focus

- Computational fluid dynamics
- Partial differential equations
- Autonomous reasoning agents
- Evidence governance and validation
- Numerical methods and GPU-aware computing
- Scientific visualization and physics rendering
- Physics-informed machine learning

## Team & License

**Founder**: Kevin Smith ([@kevmoz](https://github.com/kevmoz))
**Location**: West Yorkshire, UK
**License**: MIT (See LICENSE file)

## Contributing

POLYMATHICA follows strict engineering standards. All contributions must:
- Include working code (no placeholders)
- Pass validation governance
- Be documented and tested
- Support the core workflow pipeline

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

**From experiment to evidence. From evidence to discovery.**
