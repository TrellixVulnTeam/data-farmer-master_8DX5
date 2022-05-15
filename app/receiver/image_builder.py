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
    Builds a docker image
    """

    # extract archive
    if not os.path.exists(experiment.files_path):
        os.makedirs(experiment.files_path)

    with tarfile.open(experiment.archive_path) as file:
        file.extractall(experiment.files_path)

    # build image
    client = get_docker_client()

    image, _ = client.images.build(
        path='.',
        dockerfile=current_app.config['BASE_DOCKERFILE'],
        tag=experiment.image_tag,
        buildargs={
            "experiment_files": experiment.files_path
        }
    )

    return image
