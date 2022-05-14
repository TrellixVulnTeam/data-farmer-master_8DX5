from typing import Any

from app.model.parameter import Parameter


class Task:
    """
    Representation of a task that can be sent to a worker.
    It's important that the parameters keep the same order
    as their values in tuples.
    """

    def __init__(self, parameters: list[Parameter], values: tuple[Any]):
        self.parameters = parameters
        self.values = values
