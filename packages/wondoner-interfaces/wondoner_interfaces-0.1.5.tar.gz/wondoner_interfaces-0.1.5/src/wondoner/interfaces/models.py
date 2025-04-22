"""Models for the Wondoner interfaces module."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Dict, Any
from .enums import TaskStatus


@dataclass(frozen=True)  # Use frozen=True if Projects are immutable once created
class Project:
    """Represents a user-defined project label within the aggregator.

    Managed by the core application, not directly by plugins (plugins link tasks to it).

    """
    id: str  # Unique ID assigned by the aggregator system (e.g., UUID string)
    label: str  # The user-defined label for the project


@dataclass
class StandardTask:
    """Represents a task in a standardized format within the aggregator.

    Plugins are responsible for mapping data between the source system's
    format and this standard structure.

    """
    # --- Aggregator Metadata ---
    # Unique ID assigned by the aggregator for this specific task representation
    id: str
    # ID of the project this task belongs to (links to Project.id)
    project_id: str

    # --- Source System Metadata ---
    # The unique ID of the task in its original source system (e.g., "JIRA-123", "gh-567")
    source_id: str
    # The identifier of the source plugin (e.g., "jira", "github")
    source_name: str

    # --- Standard Task Fields ---
    name: str
    description: Optional[str] = None
    # We interpret "Date" as an optional due date. Use Optional[date].
    due_date: Optional[date] = None
    status: TaskStatus = TaskStatus.NOT_DONE  # Default to NOT_DONE

    # --- Timestamps (Often Available & Useful) ---
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # --- Raw Data (Optional) ---
    # Optionally store the original data structure from the source system
    # for debugging or advanced features. Use field to avoid it being in repr.
    raw_data: Optional[Dict[str, Any]] = field(default=None, repr=False)

    # Optional direct URL to the task in the source system
    url: Optional[str] = None

    def __post_init__(self):
        """Basic validation example (can add more if needed)"""
        if not isinstance(self.status, TaskStatus):
            raise ValueError(f"status must be a TaskStatus enum member, not {type(self.status)}")
        if not self.name:
            raise ValueError("Task name cannot be empty.")
