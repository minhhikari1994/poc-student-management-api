from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required

from ..services.unit import get_unit_by_id
from ..services.test import get_test
from ..services.test_score import get_test_score_of_a_unit

test_score_bp = Blueprint('test_score_bp', __name__)

class UnitTestScoresHandler(MethodView):
    decorators = [login_required]

    def get(self):
        unit_id = request.args.get('unit_id')
        test_id = request.args.get('test_id')

        unit = get_unit_by_id(unit_id)
        if (unit is None):
            return jsonify(
                success=False,
                message='Unit not found',
                data=None
            ), 404
        
        test = get_test(test_id)
        if (test is None):
            return jsonify(
                success=False,
                message='Test not found',
                data=None
            ), 404

        test_score_list = get_test_score_of_a_unit(test, unit)
        
        return jsonify(
            success=True,
            message='Success',
            data=list(map(lambda test_score_record: test_score_record.to_json(), test_score_list))
        ), 200
    
test_score_bp.add_url_rule(
    '/test-scores',
    view_func=UnitTestScoresHandler.as_view('unit_test_scores'),
    methods=['GET']
)
