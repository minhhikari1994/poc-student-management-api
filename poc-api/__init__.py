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
        SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
        SESSION_COOKIE_DOMAIN=os.getenv("SESSION_COOKIE_DOMAIN"),
        SESSION_COOKIE_SAME_SITE='Lax',
        SECRET_KEY=os.getenv("SECRET_KEY")
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(
        app,
        supports_credentials=True,
        origins=os.getenv("CORS_ORIGINS").split(",")
    )

    login_manager.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app, '/api')

    return app
