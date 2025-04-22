"""Enumerations for the Wondoner interfaces."""

import enum


class TaskStatus(enum.Enum):
    """
    Represents the standardized status of a task within the aggregator.
    Plugins are responsible for mapping source-specific statuses to these standard ones.

    """
    NOT_DONE = "not_done"
    DONE = "done"

    def __str__(self):
        """Return the value when casting to string."""

        return self.value
