"""PSIC Core Engine - Main orchestration engine for POLYMATHICA"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import json
from datetime import datetime


class WorkflowStatus(Enum):
    """Workflow execution status states"""
    CREATED = "created"
    CONFIGURED = "configured"
    VALIDATED = "validated"
    PREPARED = "prepared"
    RUNNING = "running"
    MONITORING = "monitoring"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


@dataclass
class ExperimentConfig:
    """Complete experiment configuration"""
    name: str
    description: str
    physics: Dict[str, Any]
    domain: Dict[str, Any]
    discretization: Dict[str, Any]
    solver: Dict[str, Any]
    monitoring: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowEvent:
    """Event in workflow execution"""
    timestamp: str
    stage: str
    status: str
    message: str
    data: Dict[str, Any] = field(default_factory=dict)


class PSICEngine:
    """Core orchestration engine for POLYMATHICA
    
    Responsibilities:
    - Orchestrate complete experiment workflows
    - Plan and validate experimental methodology
    - Track evidence and validation state
    - Manage research memory and learning
    """
    
    def __init__(self):
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.events: List[WorkflowEvent] = []
        self.evidence_store: Dict[str, Any] = {}
        
    def create_workflow(self, config: ExperimentConfig) -> str:
        """Create a new experiment workflow.
        
        Args:
            config: Experiment configuration
            
        Returns:
            Workflow ID
            
        Raises:
            ValueError: If configuration is invalid
        """
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.workflows[workflow_id] = {
            "config": config,
            "status": WorkflowStatus.CREATED,
            "created_at": datetime.now().isoformat(),
            "events": [],
        }
        
        self._log_event(
            workflow_id,
            "creation",
            WorkflowStatus.CREATED.value,
            f"Workflow created: {config.name}"
        )
        
        return workflow_id
    
    def validate_workflow(self, workflow_id: str) -> tuple[bool, List[str]]:
        """Validate workflow configuration and parameters.
        
        Args:
            workflow_id: ID of workflow to validate
            
        Returns:
            (is_valid, error_messages)
        """
        if workflow_id not in self.workflows:
            return False, [f"Workflow {workflow_id} not found"]
        
        workflow = self.workflows[workflow_id]
        config = workflow["config"]
        errors = []
        
        # Validate physics configuration
        if not config.physics:
            errors.append("Physics configuration missing")
        
        # Validate domain configuration
        if not config.domain:
            errors.append("Domain configuration missing")
        
        # Validate discretization
        if not config.discretization:
            errors.append("Discretization configuration missing")
        
        # Validate solver
        if not config.solver:
            errors.append("Solver configuration missing")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            workflow["status"] = WorkflowStatus.VALIDATED
            self._log_event(
                workflow_id,
                "validation",
                WorkflowStatus.VALIDATED.value,
                "Workflow validation passed"
            )
        else:
            self._log_event(
                workflow_id,
                "validation",
                WorkflowStatus.FAILED.value,
                f"Validation failed: {'; '.join(errors)}"
            )
        
        return is_valid, errors
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current workflow status.
        
        Args:
            workflow_id: ID of workflow
            
        Returns:
            Workflow status dictionary or None if not found
        """
        if workflow_id not in self.workflows:
            return None
        
        workflow = self.workflows[workflow_id]
        return {
            "id": workflow_id,
            "name": workflow["config"].name,
            "status": workflow["status"].value,
            "created_at": workflow["created_at"],
            "events_count": len(workflow["events"]),
        }
    
    def _log_event(self, workflow_id: str, stage: str, 
                    status: str, message: str) -> None:
        """Log a workflow event.
        
        Args:
            workflow_id: ID of workflow
            stage: Workflow stage
            status: Status at this stage
            message: Event message
        """
        event = WorkflowEvent(
            timestamp=datetime.now().isoformat(),
            stage=stage,
            status=status,
            message=message,
        )
        
        self.events.append(event)
        if workflow_id in self.workflows:
            self.workflows[workflow_id]["events"].append(event)
