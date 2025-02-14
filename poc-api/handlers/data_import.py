from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required

from ..decorators.auth import admin_required

from ..services.data_import import import_student_data, import_master_data_from_excel

data_import_bp = Blueprint('data_import_bp', __name__)

class ImportStudentData(MethodView):
    decorators = [login_required, admin_required]
    def post(self):
        student_excel_file = request.files['student_data']
        study_year_code = request.form['study_year_code']
        unit_code = request.form['unit_code']
        result = import_student_data(student_excel_file, study_year_code, unit_code)
        return jsonify(
            success=True,
            message='Success',
            data=(list(map(lambda student: student.to_json(), result)))
        ), 200
    
class ImportMasterData(MethodView):
    decorators = [login_required, admin_required]
    def post(self):
        master_excel_file = request.files['master_data']
        result = import_master_data_from_excel(master_excel_file)
        return jsonify(
            success=True,
            message='Success',
            data=[]
        ), 200

data_import_bp.add_url_rule(
    '/data-import/students',
    view_func=ImportStudentData.as_view('import_student_data_endpoint_view'),
    methods=['POST']
)

data_import_bp.add_url_rule(
    '/data-import/master',
    view_func=ImportMasterData.as_view('import_master_data_endpoint_view'),
    methods=['POST']
)