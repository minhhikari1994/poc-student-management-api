from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_login import login_required

from ..models.base import db
from ..models import Result
from ..services.unit import get_all_units, get_unit_by_id

unit_bp = Blueprint('unit_bp', __name__)

class UnitsHandler(MethodView):
    decorators = [login_required]
    
    def get(self):
        units = get_all_units()
        return jsonify(
            success=True,
            message='Success',
            data=dict(
                units=list(map(lambda unit: unit.to_json(), units))
            )
        ), 200

class UnitStudentsHandler(MethodView):
    decorators = [login_required]

    def get(self, unit_id):
        
        unit = get_unit_by_id(unit_id)
        if (unit is None):
            return jsonify(
                success=False,
                message='Unit not found',
                data=None
            ), 404
        
        unit_json = unit.to_json(
            include_student_list=True
        )

        return jsonify(
            success=True,
            message='Success',
            data=unit_json
        ), 200


units_endpoint_view = UnitsHandler.as_view('units_endpoint_view')
unit_students_endpoint_view = UnitStudentsHandler.as_view('unit_students_endpoint_view')

unit_bp.add_url_rule(
    '/units',
    view_func=units_endpoint_view,
    methods=['GET']
)

unit_bp.add_url_rule(
    '/units/<unit_id>/students',
    view_func=unit_students_endpoint_view,
    methods=['GET']
)