"""Unit tests for the enums in the wondoner.interfaces.models module."""

import pytest  # noqa: F401 - Base import needed for pytest runner, fixtures, raises, mark
from wondoner.interfaces.enums import TaskStatus


def test_task_status_enum_members():
    """Verify the TaskStatus enum has the correct members."""

    assert TaskStatus.NOT_DONE.value == "not_done"
    assert TaskStatus.DONE.value == "done"
    assert len(TaskStatus) == 2


def test_task_status_enum_str():
    """Verify the string representation of TaskStatus members."""

    assert str(TaskStatus.NOT_DONE) == "not_done"
    assert str(TaskStatus.DONE) == "done"
