# Wondoner Interfaces

![PyPI - Version](https://img.shields.io/pypi/v/wondoner-interfaces) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This package provides the core interfaces, abstract base classes, and standard data models required for building plugin integrations for the **Wondoner** task aggregator. It defines the contract that all source plugins (like for Jira, GitHub, Todoist, etc.) must adhere to.

This package is intended primarily for developers creating new plugins for Wondoner.

## Installation

```bash
pip install wondoner-interfaces
```

## Core Components

This package defines:

* `TaskSourceIntegration`: The abstract base class that all source plugins must inherit from. It defines methods for creating, reading, updating tasks, and handling change detection (polling/webhooks).
* `StandardTask`: A dataclass representing a task in a standardized format used within WonDoner. Plugins map source-specific data to this model.
* `Project`: A simple dataclass representing a project label within WonDoner.
* `TaskStatus`: An enum defining the standardized task statuses (`TaskStatus.DONE`, `TaskStatus.NOT_DONE`).

## Basic Plugin Usage

Plugin developers should inherit from TaskSourceIntegration and implement the required abstract methods:

```python
from typing import Dict, Any, Optional, AsyncGenerator

# Adjust the import based on your final package structure
from wondoner.interfaces import (
    TaskSourceIntegration,
    StandardTask,
    Project,
    TaskStatus
)

class MyCoolSourcePlugin(TaskSourceIntegration):
    # Unique identifier string for this source type
    SOURCE_NAME = "my_cool_source"

    def __init__(self, config: Dict[str, Any]):
        """Initialize with config (API keys, URLs, etc.)."""
        super().__init__(config)
        # Initialize your source-specific API client here
        # self.client = ...

    # --- Implement required abstract methods ---

    async def get_task(self, source_task_id: str) -> Optional[StandardTask]:
        # Fetch task from source API and map to StandardTask
        pass

    async def update_task(self, source_task_id: str, changes: Dict[str, Any]) -> StandardTask:
        # Update task in source API based on changes, return mapped StandardTask
        pass

    # --- Optionally override default change detection methods ---

    # async def poll_changes(self, last_sync_state: Optional[Any]) -> AsyncGenerator[StandardTask, None]:
    #     # Implement if your source requires polling
    #     pass

    # def parse_webhook_payload(self, payload: Dict[str, Any], headers: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    #     # Implement if your source uses webhooks
    #     pass
```

Please refer to the source code within this package for detailed method signatures, docstrings, and model definitions.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
