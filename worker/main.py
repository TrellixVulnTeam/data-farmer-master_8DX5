"""
Temporary worker implementation,
"""
# todo: probably move this implementation to another repository in the organization
# todo: add logs

import os
import json

import requests


def main():
    """
    PoC of getting tasks from the master's queue
    """
    host = os.getenv('MASTER_HOST')
    port = os.getenv('MASTER_PORT')
    master_url = f'http://{host}:{port}'

    number_of_tasks = 3

    res = requests.get(f'{master_url}/queue/tasks?number={number_of_tasks}')
    with open('out.txt', 'w+') as file:
        file.write(json.dumps(res.json(), indent=2))


if __name__ == '__main__':
    main()
