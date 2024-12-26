from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_login import login_required

health_check_bp = Blueprint('health_check_bp', __name__)

class HealthCheckHandler(MethodView):
    def get(self):  
        return jsonify(
            success=True,
            message='Server is up and running'
        )
    
class HealthCheckWithAuthHandler(MethodView):
    @login_required
    def get(self):
        return jsonify(
            success=True,
            message='Server is up and running'
        )

health_check_endpoint_view = HealthCheckHandler.as_view('health_check_endpoint')
health_check_with_auth_endpoint_view = HealthCheckWithAuthHandler.as_view('health_check_with_auth_endpoint')

health_check_bp.add_url_rule(
    '/health_check',
    view_func=health_check_endpoint_view,
    methods=['GET']
)

health_check_bp.add_url_rule(
    '/health_check_with_auth',
    view_func=health_check_with_auth_endpoint_view,
    methods=['GET']
)