from .handlers.health_check import health_check_bp
from .handlers.authentication import authentication_bp
from .handlers.user_account import user_account_bp

from .handlers.unit import unit_bp
from .handlers.attendance import attendance_bp
from .handlers.test import test_bp
from .handlers.test_score import test_score_bp

from .handlers.student import student_bp

from .handlers.data_import import data_import_bp

from .commands.user_commands import user_commands_bp

def register_blueprints(app, url_prefix):
    app.register_blueprint(health_check_bp, url_prefix=url_prefix)
    app.register_blueprint(authentication_bp, url_prefix=url_prefix)
    app.register_blueprint(user_account_bp, url_prefix=url_prefix)
    app.register_blueprint(unit_bp, url_prefix=url_prefix)
    app.register_blueprint(attendance_bp, url_prefix=url_prefix)
    app.register_blueprint(test_bp, url_prefix=url_prefix)
    app.register_blueprint(test_score_bp, url_prefix=url_prefix)
    app.register_blueprint(student_bp, url_prefix=url_prefix)
    app.register_blueprint(data_import_bp, url_prefix=url_prefix)
    #cli
    app.register_blueprint(user_commands_bp, cli_group="user")
