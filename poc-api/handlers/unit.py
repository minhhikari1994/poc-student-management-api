from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required

from ..models.base import db
from ..models import Result
from ..services.unit import get_all_units, get_student_list_in_a_unit

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
        result = get_student_list_in_a_unit(unit_id)
        if not result.success:
            return result.to_json(), 400
        return Result.success(result.message, dict(
            students=list(map(lambda student: student.to_json(), result.data))
        )).to_json(), 200


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