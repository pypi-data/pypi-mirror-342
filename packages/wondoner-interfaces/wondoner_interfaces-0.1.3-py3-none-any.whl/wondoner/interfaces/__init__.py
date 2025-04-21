"""This module provides an interface for task aggregation and management."""

from .interfaces import TaskSourceIntegration
from .models import StandardTask
from .enums import TaskStatus

__version__ = "0.1.3"  # Version of the interfaces module

# Controls what 'from task_aggregator_interfaces import *' imports
__all__ = [
    "TaskSourceIntegration",
    "StandardTask",
    "TaskStatus",
]
