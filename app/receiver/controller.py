"""
Endpoints for experiment receiver module
"""

import os
from flask import Blueprint, request
from docker.errors import DockerException
from app.model.experiment import Experiment
from app.model.response import Response, ResponseStatus
from app.receiver import image_builder
from app.combination import generator

receiver_blueprint = Blueprint('receiver', __name__)


@receiver_blueprint.route('/upload', methods=["POST"])
def upload() -> tuple[dict, int]:
    """
    This endpoint creates a docker image for an experiment, then it
    is uploaded to Dockerhub

    It requires tar.gz file containing at least:
        - run.sh file describing how to start an experiment
        - params.json with the definition of parameters space

    Request body:
        experiment: .tar.gz file,
        workers: number,
        tasks-per-worker: number
    """
    try:
        experiment_file = request.files['experiment']
        plugin = request.form.get('plugin')
        workers = int(request.form.get('workers'))
        tasks_per_worker = int(request.form.get('tasks_per_worker'))

        # validate request
        if not all([plugin, workers, tasks_per_worker, experiment_file]):
            raise ValueError()

        # create experiment
        experiment = Experiment(
            plugin=plugin,
            workers=workers,
            tasks_per_worker=tasks_per_worker
        )

        experiment_file.save(os.path.join(experiment.archive_path))
        _image = image_builder.build(experiment)
        tasks = generator.create_tasks(experiment.parameters_file)
        print(f"Tasks, created: {len(tasks)}")

        return Response(
            status=ResponseStatus.SUCCESS,
            data=experiment.to_json(),
            message="The experiment was successfully created").to_json(), 201
    except ValueError:
        return Response(
            status=ResponseStatus.ERROR,
            message="Incorrect request format").to_json(), 400
    except FileNotFoundError:
        return Response(
            status=ResponseStatus.ERROR,
            message="Could not save experiment file").to_json(), 500
    except DockerException as err:
        return Response(
            status=ResponseStatus.ERROR,
            message=f"Docker API error: {err}").to_json(), 500
