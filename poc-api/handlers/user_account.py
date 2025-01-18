from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required

from ..models.base import db

from ..services.user_account import create_user_account

user_account_bp = Blueprint('user_account_bp', __name__)

class UserAccountHandler(MethodView):
    def post(self):
        request_body = request.json

        login_id = request_body.get('login_id')
        password = request_body.get('password')
        is_admin = request_body.get('is_admin', False)

        is_success, message = create_user_account(login_id, password, is_admin)
        
        if not is_success:
            return jsonify(
                success=False,
                message=message
            ), 400
        
        db.session.commit()
        
        return jsonify(
            success=True,
            message=message
        ), 201


user_account_endpoint_view = UserAccountHandler.as_view('user_account_endpoint_view')
user_account_bp.add_url_rule(
    '/user-account',
    view_func=user_account_endpoint_view,
    methods=['POST']
)