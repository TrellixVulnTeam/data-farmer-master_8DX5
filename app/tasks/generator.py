"""
Logic responsible for creating a product of parameters.
"""
import itertools
from typing import Any

from app.model import parameter_definition
from app.model.task import Task


def create_tasks(parameters_definition_path: str) -> list[Task]:
    """
    Generates a list of tasks based on the product of parameters
    that were defined in the parameters' definition JSON file.
    """
    definitions = parameter_definition.from_json_file(parameters_definition_path)
    product = get_parameters_product(definitions)
    return [Task(parameter_set) for parameter_set in product]


def get_parameters_product(parameter_definitions) -> list[list[dict[str, Any]]]:
    """
    Generates a product of all parameter values based on their definitions,
    preserving the order of the parameters.
    Returns a list of unique parameter sets.
    """
    names = list(map(lambda p: p.name, parameter_definitions))
    values = list(map(lambda p: p.get_values(), parameter_definitions))
    values_product = itertools.product(*values)

    parameters_product = []
    for values_set in values_product:
        values_set_with_names = []
        for name, value in zip(names, values_set):
            values_set_with_names.append({'name': name, 'value': value})
        parameters_product.append(values_set_with_names)

    return parameters_product
