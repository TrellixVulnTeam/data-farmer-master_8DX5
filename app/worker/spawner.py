"""
Logic related to spawning workers.
"""
from docker.models.images import Image
from docker.models.containers import Container
from flask import current_app

from app import utils


def spawn(image: Image, workers: int, tasks_per_worker: int) -> list[Container]:
    """
    Spawns a given number of worker containers
    """
    client = utils.get_docker_client()
    worker_containers = []

    for i in range(workers):
        image_name = image.tags[0].split(':')[0]

        container = client.containers.run(
            image.id,
            detach=True,
            name=f'{image_name}-{i + 1}',
            environment={
                # todo: figure out what to do with it
                'MASTER_HOST': 'host.docker.internal',
                'MASTER_PORT': current_app.config['PORT'],
                'TASKS_PER_WORKER': tasks_per_worker,
                # see https://stackoverflow.com/questions/29663459/python-app-does-not-print-anything-when-running-detached-in-docker
                'PYTHONUNBUFFERED': 1
            }
        )

        worker_containers.append(container)

    return worker_containers
