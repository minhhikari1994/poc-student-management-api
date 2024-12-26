import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .models.base import db, migrate
from .helpers.auth_helper import login_manager
from .blueprints import register_blueprints

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)

    login_manager.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app, '/api')

    return app
