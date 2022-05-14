import json
from typing import Union


class Parameter:
    """
    Representation of a parameter.
    """

    def __init__(self, name: str):
        self.name = name


class NumericalParameter(Parameter):
    """
    Representation of a numerical parameter.
    """

    def __init__(self, name: str, min_val: Union[int, float], max_val: Union[int, float],
                 step: Union[int, float] = 1.0):
        Parameter.__init__(self, name)
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.step = float(step)

    def get_values(self) -> list[Union[int, float]]:
        values = []
        cur = self.min_val
        while cur <= self.max_val:
            values.append(cur)
            cur += self.step

        return values


def from_json_file(path: str) -> list[Parameter]:
    """
    Creates a parameter list from a json file
    """

    with open(path, 'r') as f:
        obj = json.load(f)
        parameters = map(from_dict, obj['parameters'])
        return list(parameters)


def from_dict(p: dict) -> Parameter:
    """
    Creates a single parameter from a dict
    """

    if p["type"] == "numerical":
        return NumericalParameter(
            name=p["name"],
            min_val=p["min"],
            max_val=p["max"],
            step=p.get("step") or 1.0
        )
    else:
        raise Exception("Unsupported parameter type")
