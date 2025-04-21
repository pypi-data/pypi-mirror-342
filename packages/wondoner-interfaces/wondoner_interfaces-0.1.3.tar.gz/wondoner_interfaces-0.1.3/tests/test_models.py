"""Unit tests for the models in the wondoner.interfaces.models module."""

import pytest
from dataclasses import FrozenInstanceError, is_dataclass
from datetime import date, datetime
from uuid import uuid4  # Using UUID for example IDs
from wondoner.interfaces.enums import TaskStatus
from wondoner.interfaces.models import Project, StandardTask


def test_project_creation_and_attributes():
    """Test creating a Project and accessing its attributes."""

    project_id = str(uuid4())
    label = "My Test Project"
    project = Project(id=project_id, label=label)

    assert is_dataclass(project)
    assert project.id == project_id
    assert project.label == label


# noinspection PyDataclass
def test_project_is_frozen():
    """Test that Project instances are immutable (frozen)."""

    project = Project(id=str(uuid4()), label="Initial Label")
    with pytest.raises(FrozenInstanceError):
        project.label = "New Label"
    with pytest.raises(FrozenInstanceError):
        project.id = str(uuid4())


def test_standard_task_creation_minimal():
    """Test creating a StandardTask with minimal required fields."""

    task_id = str(uuid4())
    project_id = str(uuid4())
    source_id = "SRC-123"
    source_name = "test_source"
    name = "Minimal Task"

    task = StandardTask(
        id=task_id,
        project_id=project_id,
        source_id=source_id,
        source_name=source_name,
        name=name,
    )

    assert is_dataclass(task)
    assert task.id == task_id
    assert task.project_id == project_id
    assert task.source_id == source_id
    assert task.source_name == source_name
    assert task.name == name
    assert task.description is None
    assert task.due_date is None
    assert task.status == TaskStatus.NOT_DONE  # Check default status
    assert task.url is None
    assert task.created_at is None
    assert task.updated_at is None
    assert task.raw_data is None


def test_standard_task_creation_full():
    """Test creating a StandardTask with all optional fields."""

    now = datetime.now()
    today = date.today()
    raw = {"key": "value"}
    task = StandardTask(
        id=str(uuid4()),
        project_id=str(uuid4()),
        source_id="SRC-456",
        source_name="test_source_2",
        name="Full Task",
        description="Detailed description.",
        due_date=today,
        status=TaskStatus.DONE,
        url="https://example.com/task/456",
        created_at=now,
        updated_at=now,
        raw_data=raw,
    )
    assert task.description == "Detailed description."
    assert task.due_date == today
    assert task.status == TaskStatus.DONE
    assert task.url == "https://example.com/task/456"
    assert task.created_at == now
    assert task.updated_at == now
    assert task.raw_data == raw


# noinspection PyTypeChecker
def test_standard_task_post_init_validation():
    """Test the __post_init__ validation logic."""

    # Test invalid status type
    with pytest.raises(ValueError, match="status must be a TaskStatus enum member"):
        StandardTask(id="t1", project_id="p1", source_id="s1", source_name="src", name="Valid Name",
                     status="done")  # Pass string instead of enum

    # Test empty name
    with pytest.raises(ValueError, match="Task name cannot be empty"):
        StandardTask(id="t2", project_id="p1", source_id="s2", source_name="src", name="")


def test_standard_task_repr_excludes_raw_data():
    """Test that raw_data is not included in the default repr."""

    task = StandardTask(
        id=str(uuid4()),
        project_id=str(uuid4()),
        source_id="SRC-789",
        source_name="test_source_3",
        name="Repr Test",
        raw_data={"lots": "of", "uninteresting": "data"},
    )
    assert "raw_data=" not in repr(task)
    # Check that other fields ARE in repr
    assert "source_id='SRC-789'" in repr(task)
    assert "name='Repr Test'" in repr(task)
