from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class ComponentNode(BaseModel):
    """
    Represents a node in the IICS Taskflow Audit graph.
    Each node corresponds to a taskflow component and contains information about its status, start time, end time, and other relevant details.
    Nodes can have different assetTypes, such as MTT, TASKFLOW.
    The node's status can be one of the following: SUCCESS, FAILURE.
    """
    
    def __repr__(self) -> str:
        # only show the “identity” of this node, not its children or root
        return (
            f"<ComponentNode run_id={self.run_id!r} "
            f"asset_type={self.asset_type!r} depth={self.depth}>"
        )
    
    # Pydantic v2 configuration
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[str] = None
    """Unique identifier for the component run."""

    run_id: str
    """The ID of the component run."""

    parent_id: Optional[str] = None
    """The ID of the parent taskflow run if this node is a subtask."""

    depth: int = 0
    """The depth of this node in the taskflow graph relative to the root node."""

    root: Optional[ComponentNode] = None
    """The root node of the taskflow graph."""

    asset_name: Optional[str] = None
    """The name of the node in the component."""
    
    asset_type: Optional[str] = None
    """The type of the asset (e.g., MTT, TASKFLOW)."""

    duration: Optional[int] = None
    """The duration of the component run in seconds."""

    start_time: Optional[str] = None
    """The startTime of the component run in ISO 8601 format."""

    end_time: Optional[str] = None
    """The endTime of the component run in ISO 8601 format."""

    update_time: Optional[str] = None
    """The time when the component was last updated in ISO 8601 format."""

    status: Optional[str] = None
    """The status of the component run (e.g., SUCCESS, FAILURE)."""

    error_message: Optional[str] = ""
    """The error message if the component run failed."""

    errored_rows: Optional[int] = 0
    """The number of errored rows in the component run."""

    location: Optional[str] = None
    """The location within Informatica Cloud where the component is located."""

    rows_processed: Optional[int] = 0
    """The number of rows processed in the component run."""

    runtime_env: Optional[str] = None
    """The runtime environment ID."""

    runtime_env_name: Optional[str] = None
    """The name of the runtime environment."""

    started_by: Optional[str] = None
    """Person who started the component run."""

    subtasks: Optional[int] = 0
    """The number of subtasks in the component run."""

    children: List[ComponentNode] = Field(default_factory=list)
    """The child nodes of this node."""
