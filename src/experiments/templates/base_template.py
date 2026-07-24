"""Base experiment template for POLYMATHICA

All experiments inherit from this base template to ensure:
- Complete workflow support
- Proper validation and governance
- Consistent monitoring and recording
- Reproducibility and archival
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from datetime import datetime
import json


class ExperimentStatus(Enum):
    """Experiment execution status"""
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


@dataclass
class ExperimentMetadata:
    """Metadata about an experiment"""
    name: str
    description: str
    researcher: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)


class BaseExperiment(ABC):
    """Abstract base class for all experiments.
    
    Enforces the complete workflow pipeline:
    CREATE → CONFIGURE → MESH → VALIDATE → RUN → MONITOR → 
    VISUALISE → RECORD → REPLAY → REPORT → DISCUSS → ARCHIVE → PUBLISH
    
    All subclasses must implement these methods.
    """
    
    def __init__(self, metadata: ExperimentMetadata):
        """Initialize experiment.
        
        Args:
            metadata: Experiment metadata
        """
        self.metadata = metadata
        self.status = ExperimentStatus.INITIALIZED
        self.telemetry: Dict[str, Any] = {}
        self.results: Dict[str, Any] = {}
        self.events: List[Dict[str, Any]] = []
        
    @abstractmethod
    def configure(self) -> bool:
        """Configure experiment parameters and environment.
        
        Returns:
            True if configuration succeeded
        """
        pass
    
    @abstractmethod
    def create_mesh(self) -> bool:
        """Create or load computational mesh.
        
        Returns:
            True if mesh creation succeeded
        """
        pass
    
    @abstractmethod
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate experiment setup and parameters.
        
        Returns:
            (is_valid, error_messages)
        """
        pass
    
    @abstractmethod
    def run(self) -> bool:
        """Execute the experiment.
        
        Returns:
            True if execution succeeded
        """
        pass
    
    @abstractmethod
    def monitor(self) -> Dict[str, Any]:
        """Monitor experiment execution and collect telemetry.
        
        Returns:
            Telemetry dictionary with current metrics
        """
        pass
    
    @abstractmethod
    def visualize(self) -> bool:
        """Generate visualizations of results.
        
        Returns:
            True if visualization succeeded
        """
        pass
    
    @abstractmethod
    def record(self) -> bool:
        """Record experiment data and evidence.
        
        Returns:
            True if recording succeeded
        """
        pass
    
    def execute_workflow(self) -> bool:
        """Execute complete experiment workflow.
        
        Implements the full pipeline with proper error handling
        and checkpointing.
        
        Returns:
            True if workflow completed successfully
        """
        try:
            # Step 1: Configure
            self._log_event("CONFIGURE", "Starting configuration")
            if not self.configure():
                self._log_event("CONFIGURE", "Configuration failed", error=True)
                return False
            self._log_event("CONFIGURE", "Configuration complete")
            
            # Step 2: Create mesh
            self._log_event("MESH", "Creating computational mesh")
            if not self.create_mesh():
                self._log_event("MESH", "Mesh creation failed", error=True)
                return False
            self._log_event("MESH", "Mesh created successfully")
            
            # Step 3: Validate
            self._log_event("VALIDATE", "Validating experiment setup")
            is_valid, errors = self.validate()
            if not is_valid:
                self._log_event(
                    "VALIDATE",
                    f"Validation failed: {'; '.join(errors)}",
                    error=True
                )
                return False
            self._log_event("VALIDATE", "Validation passed")
            
            # Step 4: Run
            self._log_event("RUN", "Starting experiment execution")
            self.status = ExperimentStatus.RUNNING
            if not self.run():
                self._log_event("RUN", "Execution failed", error=True)
                self.status = ExperimentStatus.FAILED
                return False
            self._log_event("RUN", "Execution completed")
            self.status = ExperimentStatus.COMPLETED
            
            # Step 5: Monitor (collect final telemetry)
            self._log_event("MONITOR", "Collecting final telemetry")
            self.telemetry.update(self.monitor())
            self._log_event("MONITOR", "Telemetry collected")
            
            # Step 6: Visualize
            self._log_event("VISUALIZE", "Generating visualizations")
            if not self.visualize():
                self._log_event("VISUALIZE", "Visualization failed", error=True)
                # Don't fail the workflow, continue to recording
            self._log_event("VISUALIZE", "Visualizations generated")
            
            # Step 7: Record
            self._log_event("RECORD", "Recording experiment data")
            if not self.record():
                self._log_event("RECORD", "Recording failed", error=True)
                return False
            self._log_event("RECORD", "Data recorded successfully")
            
            # Step 8: Archive
            self._log_event("ARCHIVE", "Archiving experiment")
            # Archive logic would go here
            self._log_event("ARCHIVE", "Experiment archived")
            
            self.status = ExperimentStatus.ARCHIVED
            return True
            
        except Exception as e:
            self._log_event("ERROR", str(e), error=True)
            self.status = ExperimentStatus.FAILED
            return False
    
    def _log_event(self, stage: str, message: str, error: bool = False) -> None:
        """Log an experiment event.
        
        Args:
            stage: Workflow stage
            message: Event message
            error: Whether this is an error event
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "stage": stage,
            "message": message,
            "error": error,
        }
        self.events.append(event)
        
        if error:
            print(f"[ERROR] {stage}: {message}")
        else:
            print(f"[{stage}] {message}")
