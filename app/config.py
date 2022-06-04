# pylint: skip-file
"""
Flask config for different environments
"""

import os


class Config:
    DEBUG = False
    TESTING = False
    UPLOADS_DIR = os.getenv('UPLOADS_DIR') or './uploads'
    DOCKER_BASE_URL = os.getenv('DOCKER_BASE_URL') or "unix:///var/run/docker.sock"
    WORKER_BASE_DOCKERFILE = os.getenv('WORKER_BASE_DOCKERFILE') or "./images/Dockerfile.worker"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
