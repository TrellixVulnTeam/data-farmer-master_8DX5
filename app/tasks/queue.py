"""
Logic related to queueing tasks that workers can access.
"""

from collections import deque

from flask import Blueprint
from flask import request

from app.model.response import Response, ResponseStatus
from app.model.task import Task


class TaskQueueMeta(type):
    """
    Metaclass used to implement the Singleton pattern.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TaskQueue(metaclass=TaskQueueMeta):
    """
    A global queue of tasks that workers can access through the API.
    Currently, lacks distinguishing from which experiment a task comes from.
    """

    def __init__(self):
        self.tasks = deque()

    def add(self, task: Task):
        """
        Adds one task to the end of the queue
        """
        self.tasks.append(task)

    def extend(self, tasks: list[Task]):
        """
        Extends a queue with the tasks from the list on its right
        """
        self.tasks.extend(tasks)

    def take(self, number: int = 1) -> list[Task]:
        """
        Takes {number} of tasks from the beginning of the queue.
        Can result in an empty list or a list of less than {number} tasks.
        """
        result = []
        taken = 0
        while taken < number and len(self.tasks) > 0:
            result.append(self.tasks.popleft())
            taken += 1

        return result


queue_blueprint = Blueprint('queue', __name__)


@queue_blueprint.route('/tasks', methods=["GET"])
def get_tasks():
    """
    Returns a specified number of tasks from the beginning
    of the tasks queue.
    """
    number = request.args.get('number')
    # todo: handle missing number parameter
    tasks = TaskQueue().take(int(number))

    return Response(
        status=ResponseStatus.SUCCESS,
        data=tasks,
    ).to_json(), 200, {'Content-Type': 'application/json'}
