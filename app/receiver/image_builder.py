"""
Module responsible for creating a docker image for a new experiment
"""

import tarfile
import os


def build(path: str):
    """
    Builds a docker image
    """
    extract(path)


def extract(path: str):
    """
    Extracts files from tar.gz archive
    """
    content_path = path + '-content'
    if not os.path.exists(content_path):
        os.makedirs(content_path)

    with tarfile.open(path) as file:
        file.extractall(content_path)
