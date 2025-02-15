from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from ..services.user_account import login, logout
from ..models.base import db

authentication_bp = Blueprint('authentication_bp', __name__)

class LoginHandler(MethodView):
    @login_required
    def get(self):
        return jsonify(
            success=True,
            message='Bạn đã đăng nhập rồi',
            data=dict(
                name=current_user.login_id.split('@')[0],
                email=current_user.login_id
            )
        ), 200

    def post(self):
        request_body = request.json
        login_result, message = login(
            request_body.get('login_id'),
            request_body.get('password')
        )
        if not login_result:
            return jsonify(
                success=False,
                message=message
            ), 401
        
        db.session.commit()

        return jsonify(
            success=True,
            message=message,
            data=dict(
                name=current_user.login_id.split('@')[0],
                email=current_user.login_id
            )
        ), 200

class LogoutHandler(MethodView):
    decorators = [login_required]

    def post(self):
        is_success, message = logout()
        return jsonify(
            success=True,
            message=message
        ), 200

login_endpoint_view = LoginHandler.as_view('login_endpoint')
logout_endpoint_view = LogoutHandler.as_view('logout_endpoint')

authentication_bp.add_url_rule(
    '/login',
    view_func=login_endpoint_view,
    methods=['POST']
)
authentication_bp.add_url_rule(
    '/auth_check',
    view_func=login_endpoint_view,
    methods=['GET']
)
authentication_bp.add_url_rule(
    '/logout',
    view_func=logout_endpoint_view,
    methods=['POST']
)