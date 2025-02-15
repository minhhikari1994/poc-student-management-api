from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required

from ..services.unit import get_unit_by_id
from ..services.test import get_test_list_for_a_unit

test_bp = Blueprint('test_bp', __name__)

class TestHandler(MethodView):
    decorators = [login_required]

    def get(self, unit_id):

        unit = get_unit_by_id(unit_id)
        if (unit is None):
            return jsonify(
                success=False,
                message='Không tìm thấy lớp học',
                data=None
            ), 404
        
        test_list = get_test_list_for_a_unit(unit)
        
        return jsonify(
            success=True,
            message='Success',
            data=list(map(lambda test: test.to_json(), test_list))
        ), 200
    
test_bp.add_url_rule(
    '/tests/<unit_id>',
    view_func=TestHandler.as_view('test'),
    methods=['GET']
)
