import os
from grattitude.config import config_env_files
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='development', p_db=db):
    new_app = Flask(__name__)
    config_app(config_name, new_app)
    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    p_db.init_app(new_app)
    return new_app

def config_app(config_name, new_app):
    new_app.config.from_object(config_env_files[config_name])

app = create_app()

import grattitude.views
