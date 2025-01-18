from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required

from ..models.base import db
from ..services.unit import get_all_units

unit_bp = Blueprint('unit_bp', __name__)

class UnitsHandler(MethodView):
    decorators = [login_required]
    
    def get(self):
        units = get_all_units()
        return jsonify(
            success=True,
            message='Success',
            data=list(map(lambda unit: unit.to_json(), units))
        ), 200


units_endpoint_view = UnitsHandler.as_view('units_endpoint_view')
unit_bp.add_url_rule(
    '/units',
    view_func=units_endpoint_view,
    methods=['GET']
)