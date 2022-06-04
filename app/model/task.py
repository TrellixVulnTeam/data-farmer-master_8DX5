"""
Logic related to creating and interacting with tasks.
"""

from typing import Any

from app import combination
from app.model import parameter_definition
from app.model.parameter_definition import ParameterDefinition


class Task:
    """
    Representation of a task that can be sent to a worker.
    It's important that the parameter definitions keep the same order
    as their values in tuples.
    """

    def __init__(self, parameter_definitions: list[ParameterDefinition], values: tuple[Any]):
        self.parameters = parameter_definitions
        self.values = values


def create_tasks(parameters_definition_path: str) -> list[Task]:
    """
    Generates a list of tasks based on the product of parameters
    that were defined in the parameters' definition JSON file.
    """
    parameter_definitions = parameter_definition.from_json_file(parameters_definition_path)
    product = combination.generator.get_parameters_product(parameter_definitions)
    return [Task(parameter_definitions, values) for values in product]
