from flask import jsonify
from flask_login import LoginManager

from ..models import UserAccount

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(
        success=False,
        message='Unauthorized access'
    ), 401