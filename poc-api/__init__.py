import os, sentry_sdk
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .models.base import db, migrate
from .helpers.auth_helper import login_manager
from .blueprints import register_blueprints

def init_sentry():
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        _experiments={
            # Set continuous_profiling_auto_start to True
            # to automatically start the profiler on when
            # possible.
            "continuous_profiling_auto_start": True,
        },
    )

def create_app(test_config=None):
    load_dotenv()

    if os.environ.get('SENTRY_DSN'):
        init_sentry()
    
    app = Flask(__name__, instance_relative_config=True)

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
