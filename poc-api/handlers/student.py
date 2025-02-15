import datetime

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required

from ..services.student import get_student_by_student_code
from ..services.test_score import get_test_score_of_a_student_in_a_grade
from ..services.attendance import get_attendance_data_of_a_student

student_bp = Blueprint('student_bp', __name__)

class StudentSummaryHandler(MethodView):
    decorators = [login_required]
    def get(self, student_code):
        grade_code = request.args.get('grade_code')

        existing_student = get_student_by_student_code(student_code)
        if existing_student is None:
            return jsonify(
                success=False,
                message='Student not found',
                data=None
            ), 404
        
        student_test_scores = get_test_score_of_a_student_in_a_grade(existing_student, grade_code)
        student_attendance = get_attendance_data_of_a_student(
            existing_student,
            datetime.date(2024, 9, 1),
            datetime.date.today(),
        )

        return jsonify(
            success=True,
            message='',
            data=dict(
                student_info = existing_student.to_json(),
                test_scores = student_test_scores,
                attendances = student_attendance
            )
        ), 200

student_bp.add_url_rule(
    '/students/<student_code>',
    view_func=StudentSummaryHandler.as_view('student_summary'),
    methods=['GET']
)