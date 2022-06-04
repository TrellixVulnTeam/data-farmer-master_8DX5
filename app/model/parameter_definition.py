"""
Classes representing parsed parameters from
a parameter configuration JSON file.
"""

import json
from typing import Union


class ParameterDefinition:
    """
    Representation of a parameter definition.
    """

    def __init__(self, name: str):
        self.name = name


class NumericalParameterDefinition(ParameterDefinition):
    """
    Representation of a numerical parameter definition.
    """

    def __init__(self, name: str, min_val: Union[int, float], max_val: Union[int, float],
                 step: Union[int, float] = 1.0):
        ParameterDefinition.__init__(self, name)
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.step = float(step)

    def get_values(self) -> list[Union[int, float]]:
        """
        Generates all possible values from min to max iterating by a step
        """
        values = []
        cur = self.min_val
        while cur <= self.max_val:
            values.append(cur)
            cur += self.step

        return values


def from_json_file(path: str) -> list[ParameterDefinition]:
    """
    Creates a parameter definitions list from a JSON file
    """

    with open(path, 'r', encoding='utf-8') as file:
        obj = json.load(file)
        parameters = map(from_dict, obj['parameters'])
        return list(parameters)


def from_dict(parameter: dict) -> ParameterDefinition:
    """
    Creates a single parameter from a dict
    """

    if parameter["type"] == "numerical":
        return NumericalParameterDefinition(
            name=parameter["name"],
            min_val=parameter["min"],
            max_val=parameter["max"],
            step=parameter.get("step") or 1.0
        )

    raise Exception("Unsupported parameter type")
