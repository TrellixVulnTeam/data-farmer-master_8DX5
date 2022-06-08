"""
Module responsible for creating a docker image for a new experiment
"""

import tarfile
import os
from docker.models.images import Image
from flask import current_app
from app.utils import get_docker_client
from app.model.experiment import Experiment


def build(experiment: Experiment) -> Image:
    """
    Builds a Docker image of a worker
    """
    paths = experiment.get_paths()

    # extract archive
    if not os.path.exists(paths['files_path']):
        os.makedirs(paths['files_path'])

    with tarfile.open(experiment.archive_path) as file:
        file.extractall(paths['files_path'])

    # build image
    client = get_docker_client()

    image, _ = client.images.build(
        path='.',
        dockerfile=current_app.config['WORKER_BASE_DOCKERFILE'],
        tag=experiment.get_image_tag(),
        rm=True,
        buildargs={
            "experiment_files": paths['files_path']
        }
    )

    return image
