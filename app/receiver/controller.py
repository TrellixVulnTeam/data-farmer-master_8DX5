"""
Endpoints for experiment receiver module
"""

import os
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from app.model.response import Response, ResponseStatus
from app.receiver import image_builder

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
    file = request.files['experiment']
    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOADS_DIR'], filename))

    plugin = request.form.get('plugin')
    workers = int(request.form.get('workers'))
    tasks_per_worker = int(request.form.get('tasks_per_worker'))

    if not all([plugin, workers, tasks_per_worker]):
        return Response(
            status=ResponseStatus.ERROR,
            message="Please provide all three: plugin, workers and tasks_per_worker").to_json(), 400

    image_builder.build(current_app.config['UPLOADS_DIR'] + '/' + filename)

    return Response(
        status=ResponseStatus.SUCCESS,
        message="The experiment was successfully created").to_json(), 201
