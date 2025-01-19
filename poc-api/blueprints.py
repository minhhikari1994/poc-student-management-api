from .handlers.health_check import health_check_bp
from .handlers.authentication import authentication_bp
from .handlers.user_account import user_account_bp

from .handlers.unit import unit_bp

from .handlers.data_import import data_import_bp

def register_blueprints(app, url_prefix):
    app.register_blueprint(health_check_bp, url_prefix=url_prefix)
    app.register_blueprint(authentication_bp, url_prefix=url_prefix)
    app.register_blueprint(user_account_bp, url_prefix=url_prefix)
    app.register_blueprint(unit_bp, url_prefix=url_prefix)
    app.register_blueprint(data_import_bp, url_prefix=url_prefix)
