import itertools

from app.model import parameter
from app.model.task import Task


def get_parameter_space(parameters):
    values = map(lambda p: p.get_values(), parameters)
    space = itertools.product(*values)
    return list(space)


def create_tasks(parameters_file_path: str):
    parameters = parameter.from_json_file(parameters_file_path)
    space = get_parameter_space(parameters)
    return [Task(parameters, values) for values in space]
