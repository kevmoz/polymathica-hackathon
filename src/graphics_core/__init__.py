"""Graphics Core - Scientific visualization and instrumentation

Provides:
- Real-time scientific rendering
- Interactive instrumentation dashboards
- Publication-quality visualizations
- Simulation recording and replay
"""

__version__ = "0.1.0"

from .rendering import RenderingEngine
from .visualization import Plotter

__all__ = [
    "RenderingEngine",
    "Plotter",
]
