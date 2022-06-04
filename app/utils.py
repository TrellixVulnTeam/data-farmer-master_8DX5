"""
Various utilities used throughout the application.
"""

from docker import DockerClient
from flask import current_app


def get_docker_client() -> DockerClient:
    """
    :return: A DockerClient instance
    """
    return DockerClient(base_url=current_app.config['DOCKER_BASE_URL'])
