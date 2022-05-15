# pylint: skip-file
"""
Flask config for different environments
"""

import os

class Config(object):
    DEBUG = False
    TESTING = False
    UPLOADS_DIR = os.getenv('UPLOADS_DIR') or './uploads'
    DOCKER_BASE_URL = os.getenv('DOCKER_BASE_URL') or "unix:///var/run/docker.sock"
    BASE_DOCKERFILE = os.getenv('BASE_DOCKERFILE') or "./base_dockerfile/Dockerfile"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
