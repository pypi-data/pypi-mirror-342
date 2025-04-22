"""
wondoner - Task Aggregator

A task aggregator that integrates with various source systems (e.g., Jira, GitHub) to manage tasks in a standardized
format.

This module defines the abstract base class for all source integrations (plugins).

This file is part of the Wondoner project.

"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, AsyncGenerator, ClassVar

# Import the models and enums from sibling files within the same package
from .models import StandardTask
from .enums import TaskStatus  # noqa: F401 - Imported for type clarity in docstrings/dicts


class TaskSourceIntegration(ABC):
    """Abstract Base Class defining the contract for all source integrations (plugins).

    Each plugin implementation must inherit from this class and implement all
    abstract methods to interact with its specific source system (e.g., Jira, GitHub).
    It uses standardized models like StandardTask where appropriate.

    """
    # --- Class Attribute ---
    # Each concrete plugin implementation MUST override this class variable.
    # It's used by the core application to identify the plugin type.
    SOURCE_NAME: ClassVar[str] = "unknown"

    # --- Initialization ---
    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        """Initializes the integration plugin instance.

        Called by the core application when loading an enabled plugin for a user.

        Args:
            config: A dictionary containing configuration specific to this source
                    and potentially the user context (e.g., API tokens/keys fetched
                    securely, API base URLs, project keys/IDs relevant to the source).
                    Secrets required for authentication should be present here,
                    having been resolved by the core application (e.g., from Key Vault).

        """
        self.config = config
        # Concrete implementations should initialize their specific API clients here
        # using credentials and settings found in the self.config dictionary.
        # Example: self.api_client = SourceApiClient(token=self.config['api_token'])

    # --- Core CRUD Operations ---
    @abstractmethod
    async def get_task(self, source_task_id: str) -> Optional[StandardTask]:
        """
        Fetches the current state of a single task from the source system
        using its native ID.

        Args:
            source_task_id: The unique identifier of the task within the source system.

        Returns:
            A StandardTask object representing the task's current state, mapped
            to the standard format. Returns None if the task cannot be found or
            accessed with the provided configuration/credentials.

        """
        pass

    @abstractmethod
    async def update_task(self, source_task_id: str, changes: Dict[str, Any]) -> StandardTask:
        """
        Updates an existing task in the source system based on standardized changes.

        Args:
            source_task_id: The unique identifier of the task within the source system.
            changes: A dictionary where keys are standardized field names defined in
                     StandardTask (e.g., 'name', 'description', 'status', 'due_date')
                     and values are the new target values. For status, the value
                     should be a TaskStatus enum member. The plugin should only
                     attempt to update the fields present in this dictionary.

        Returns:
            A StandardTask object representing the full state of the task *after*
            the update has been successfully applied in the source system.

        Raises:
            Exception: If the task update fails (e.g., task not found, invalid data,
                       permissions error, API error). Specific exception types
                       are recommended.

        """
        pass

    # --- Change Detection Methods (Implement based on source capabilities) ---
    async def poll_changes(self, last_sync_state: Optional[Any]) -> AsyncGenerator[StandardTask, None]:
        """Polls the source system for tasks created or updated since the last sync point.

        (Optional: Implement only if the source requires polling for changes)

        Args:
            last_sync_state: Opaque data representing the state from the previous poll
                             (e.g., a timestamp, sequence ID, sync token). Defined and
                             interpreted solely by the plugin implementation.
                             `None` typically indicates an initial sync.

        Yields:
            StandardTask: For each task identified as new or changed since the
                          'last_sync_state', yields the task's current state mapped
                          to the StandardTask format.

        Note:
            The plugin should handle pagination internally if the source API uses it.
            It should ideally return a new sync state marker after completion if needed,
            though this ABC doesn't mandate how that state is managed externally.

        """
        # Default implementation raises NotImplementedError if called but not overridden.
        raise NotImplementedError(f"{self.__class__.__name__} does not support polling.")

    def parse_webhook_payload(
            self, payload: Dict[str, Any], headers: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        (Optional: Implement only if the source uses webhooks for change notifications)
        Parses and validates an incoming webhook payload from the source system.

        Args:
            payload: The parsed (usually JSON) payload from the webhook request body.
            headers: A dictionary of the HTTP headers from the webhook request. Useful
                     for validation like checking HMAC signatures using secrets
                     stored in self.config.

        Returns:
            A dictionary representing the standardized change event if the webhook is
            valid and relevant. The dictionary structure should be defined by convention,
            but could include keys like:
                - 'event_type': str ('created', 'updated', 'deleted')
                - 'source_task_id': str
                - 'timestamp': Optional[datetime] (When the event occurred)
                - 'changed_fields': Optional[Dict[str, Any]] (For 'updated' events)
            Returns None if the webhook payload is invalid (e.g., signature mismatch),
            cannot be parsed, represents an event type the aggregator doesn't care
            about, or is otherwise irrelevant.

        """
        # Default implementation assumes no webhook support.
        raise NotImplementedError(f"{self.__class__.__name__} does not support webhooks.")
