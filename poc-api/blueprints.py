from .handlers.health_check import health_check_bp
from .handlers.authentication import authentication_bp
from .handlers.user_account import user_account_bp

def register_blueprints(app, url_prefix):
    app.register_blueprint(health_check_bp, url_prefix=url_prefix)
    app.register_blueprint(authentication_bp, url_prefix=url_prefix)
    app.register_blueprint(user_account_bp, url_prefix=url_prefix)
