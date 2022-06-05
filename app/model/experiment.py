"""
Logic related to dealing with an experiment data structure
"""

import uuid
from flask import current_app


class Experiment:
    """
    Experiment data structure
    """

    def __init__(self, plugin: str, workers: int, tasks_per_worker: int):
        self.uuid = str(uuid.uuid4())
        self.archive_path = f"{current_app.config['UPLOADS_DIR']}/{self.uuid}.tar.gz"
        self.plugin = plugin
        self.workers = workers
        self.tasks_per_worker = tasks_per_worker
        self.worker_containers = []

    def get_image_tag(self):
        """
        Returns an image tag that the worker spawning module
        will use to tag its workers
        """
        return f"data-farmer-experiment-{self.uuid}"

    def get_paths(self):
        """
        Returns paths to the extracted archive content,
        the JSON parameters definition file
        and the script that runs user's program
        """
        files_path = self.archive_path + "-content"

        return {
            "files_path": files_path,
            "parameters_definition_path": files_path + "/params.json",
            "run_file": files_path + "/run.sh"
        }
