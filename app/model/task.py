"""
Logic related to creating and interacting with tasks.
"""
import uuid
from typing import Any


class Task:
    """
    Representation of a task that can be sent to a worker.
    """

    def __init__(self, parameter_set: list[dict[str, Any]]):
        self.uuid = str(uuid.uuid4())
        self.parameter_set = parameter_set
