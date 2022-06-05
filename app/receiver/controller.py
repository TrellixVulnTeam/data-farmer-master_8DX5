"""
Endpoints for experiment receiver module
"""

import os
from flask import Blueprint, request
from docker.errors import DockerException
from app.model.experiment import Experiment
from app.model.response import Response, ResponseStatus
from app.receiver import image_builder
from app.tasks import generator
from app.tasks.queue import TaskQueue

receiver_blueprint = Blueprint('receiver', __name__)


@receiver_blueprint.route('/upload', methods=["POST"])
def upload():
    """
    This endpoint creates a Docker image for an experiment, then it
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

        paths = experiment.get_paths()
        experiment_file.save(os.path.join(experiment.archive_path))

        # build worker docker image
        _image = image_builder.build(experiment)

        # create tasks out of the parameters
        tasks = generator.create_tasks(paths['parameters_definition_path'])
        task_queue = TaskQueue()
        task_queue.extend(tasks)

        return Response(
            status=ResponseStatus.SUCCESS,
            data=experiment,
            message=f"The experiment was successfully created. Tasks: {len(tasks)}"
        ).to_json(), 201, {'Content-Type': 'application/json'}
    except ValueError:
        return Response(
            status=ResponseStatus.ERROR,
            message="Incorrect request format"
        ).to_json(), 400, {'Content-Type': 'application/json'}
    except FileNotFoundError:
        return Response(
            status=ResponseStatus.ERROR,
            message="Could not save experiment file"
        ).to_json(), 500, {'Content-Type': 'application/json'}
    except DockerException as err:
        return Response(
            status=ResponseStatus.ERROR,
            message=f"Docker API error: {err}"
        ).to_json(), 500, {'Content-Type': 'application/json'}
