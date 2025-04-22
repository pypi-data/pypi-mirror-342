"""Unit tests for the TaskSourceIntegration interface."""

import pytest
import abc
from typing import Dict, Any, Optional
from wondoner.interfaces import TaskSourceIntegration  # Use __init__.py export
from wondoner.interfaces.models import StandardTask


def test_task_source_integration_is_abc():
    """Verify TaskSourceIntegration is an Abstract Base Class."""

    assert issubclass(TaskSourceIntegration, abc.ABC)


def test_task_source_integration_cannot_instantiate():
    """Verify the ABC cannot be instantiated directly and key methods are abstract."""

    # Directly attempt instantiation inside the context manager
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        TaskSourceIntegration(config={})  # <--- Replace 'pass' with this line

    # You can keep the checks below as complementary verification
    # Check that the methods requiring overrides in subclasses are abstract
    abstract_methods = TaskSourceIntegration.__abstractmethods__
    required_methods_for_concrete = {"get_task", "update_task"}

    # Verify that the set of abstract methods includes all the ones we require
    assert abstract_methods.issuperset(required_methods_for_concrete)

    # Check SOURCE_NAME class attribute exists on the ABC
    assert hasattr(TaskSourceIntegration, 'SOURCE_NAME')


# --- Test Default Method Implementations ---

class MinimalPlugin(TaskSourceIntegration):
    """Minimal concrete implementation of TaskSourceIntegration for testing."""

    SOURCE_NAME = "minimal_test"  # Must define SOURCE_NAME

    # Provide concrete implementations for required abstract methods
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)  # Call ABC __init__

    async def get_task(self, source_task_id: str) -> Optional[StandardTask]:
        raise NotImplementedError("Minimal get_task")  # Dummy implementation

    async def update_task(self, source_task_id: str, changes: Dict[str, Any]) -> StandardTask:
        raise NotImplementedError("Minimal update_task")  # Dummy implementation

    # We inherit the default implementations of poll_changes and parse_webhook_payload


@pytest.mark.asyncio
async def test_default_poll_changes_raises_not_implemented():
    """Test that awaiting the default poll_changes raises NotImplementedError."""
    plugin = MinimalPlugin(config={})

    expected_error_pattern = f"{MinimalPlugin.__name__} does not support polling"
    # expected_error_pattern = rf"{MinimalPlugin.__name__} does not support polling\."

    with pytest.raises(NotImplementedError, match=expected_error_pattern):
        await plugin.poll_changes(last_sync_state=None)


def test_default_parse_webhook_payload_raises_not_implemented():
    """Test that calling the default parse_webhook_payload raises NotImplementedError."""
    plugin = MinimalPlugin(config={})
    expected_error_msg = f"{MinimalPlugin.__name__} does not support webhooks"
    with pytest.raises(NotImplementedError, match=expected_error_msg):
        plugin.parse_webhook_payload(payload={}, headers={})
