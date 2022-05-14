# pylint: skip-file
"""
Flask config for different environments
"""


class Config(object):
    DEBUG = False
    UPLOADS_DIR = './uploads'
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
