import uuid
import json
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

        self.files_path = self.archive_path + "-content"
        self.image_tag = f"data-farmer-experiment-{self.uuid}"
        self.parameters_file = self.files_path + "/params.json"
        self.run_file = self.files_path + "/run.sh"

    def to_json(self) -> str:
        """
        Json parser
        """
        return json.dumps(self.__dict__)
