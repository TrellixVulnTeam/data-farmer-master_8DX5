"""
Logic responsible for creating a product of parameters.
"""
import itertools


def get_parameters_product(parameter_definitions):
    """
    Generates a product of all parameter values based on their definitions,
    preserving the order of the parameters.
    """
    values = map(lambda p: p.get_values(), parameter_definitions)
    product = itertools.product(*values)
    return list(product)
