"""
Setup of flask application
"""

import os
from flask import Flask
from app.receiver.controller import receiver_blueprint
from app.tasks.queue import queue_blueprint

from . import tasks, model, receiver

__all__ = [tasks, model, receiver]

app = Flask(__name__)

# Pick config for current env
ENV = os.getenv('ENV')

if ENV == 'production':
    app.config.from_object('configuration.ProductionConfig')
elif ENV == 'test':
    app.config.from_object('configuration.TestingConfig')
else:
    app.config.from_object('app.config.DevelopmentConfig')

# check if the directory for files uploaded via receiver exists - if not create it
if not os.path.exists(app.config['UPLOADS_DIR']):
    os.makedirs(app.config['UPLOADS_DIR'])

app.register_blueprint(receiver_blueprint, url_prefix='/receiver')
app.register_blueprint(queue_blueprint, url_prefix='/queue')
