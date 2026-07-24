"""PSIC - Polymath Scientific Intelligence Core

The orchestration, reasoning, and governance engine for POLYMATHICA.

Provides:
- Experiment planning and workflow orchestration
- Methodology reasoning and validation
- Evidence governance and tracking
- Research memory and learning systems
"""

__version__ = "0.1.0"

from .core import PSICEngine
from .reasoning import ExperimentPlanner, MethodologyValidator
from .validation import GovernanceEngine, EvidenceValidator

__all__ = [
    "PSICEngine",
    "ExperimentPlanner",
    "MethodologyValidator",
    "GovernanceEngine",
    "EvidenceValidator",
]
