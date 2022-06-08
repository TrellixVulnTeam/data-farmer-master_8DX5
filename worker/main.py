"""
Temporary worker implementation,
"""
# todo: probably move this implementation to another repository in the organization
# todo: add logs

import os
import json
import subprocess
import time
from threading import Thread

import requests


def get_tasks(master_url: str, number: int):
    """
    Requests a given number of tasks from the master's general queue
    """
    res = requests.get(f'{master_url}/queue/tasks?number={number}')
    return res.json()['data']


def run_task(task):
    """
    Runs a subprocess that executes user's program with given parameters
    """
    program_args = list(map(lambda p: str(p["value"]), task["parameter_set"]))
    res = subprocess.run(["sh", "run.sh"] + program_args, cwd="./files",
                         capture_output=True, check=True)

    with open(f'./out/task_{task["uuid"]}.txt', 'wb') as file:
        file.write(res.stdout)


def spawn_threads(tasks):
    threads = []
    for task in tasks:
        t = Thread(target=run_task, args=(task,))
        threads.append(t)
        t.start()

    return threads


def save_duration(duration, use_threads):
    with open(f'./out/duration.txt', 'w+') as file:
        file.write(f'Duration: {duration} s, using threads: {use_threads}\n')


def main():
    """
    PoC of getting tasks from the master's queue
    """
    host = os.getenv('MASTER_HOST')
    port = os.getenv('MASTER_PORT')
    master_url = f'http://{host}:{port}'

    tasks_per_worker = int(os.getenv('TASKS_PER_WORKER'))

    os.mkdir('out')

    use_threads = True
    start = time.time()

    # todo: get tasks_per_worker from env
    tasks = get_tasks(master_url, tasks_per_worker)
    while len(tasks) > 0:
        try:
            if use_threads:
                task_threads = spawn_threads(tasks)
                for t in task_threads:
                    t.join()
            else:
                for task in tasks:
                    run_task(task)

            tasks = get_tasks(master_url, tasks_per_worker)
        except Exception as err:
            print("Error")
            print(err)
            # todo: remove sleep
            time.sleep(3600)

    duration = time.time() - start
    save_duration(duration, use_threads)

    print("Success")
    # todo: remove sleep
    time.sleep(3600)


if __name__ == '__main__':
    main()
