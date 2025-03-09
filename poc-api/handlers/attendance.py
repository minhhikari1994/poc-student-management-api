import datetime
from flask import Blueprint, jsonify, request, send_file
from flask.views import MethodView
from flask_login import login_required

from ..models.base import db

from ..services.unit import get_unit_by_id
from ..services.attendance import get_attendance_data_for_a_unit, create_or_update_student_attendance, get_unit_attendance_report_data
from ..services.student import get_student_by_student_code

from ..services.data_export import export_unit_attendance_report_to_excel

from ..helpers.enums import AttendanceStatusEnum

attendance_bp = Blueprint('attendance_bp', __name__)

class AttendancesHandler(MethodView):
    decorators = [login_required]

    def get(self):

        attendance_date_from_req = request.args.get('date')
        attendance_unit = request.args.get('unit')
        
        try:
            attendance_date = datetime.datetime.strptime(attendance_date_from_req, '%Y%m%d').date()
        except ValueError:
            return jsonify(
                success=False,
                message='Ngày điểm danh phải ở định dạng YYYYMMDD'
            ), 400

        unit = get_unit_by_id(attendance_unit)

        if (unit is None):
            return jsonify(
                success=False,
                message='Không tìm thấy lớp học',
                data=None
            ), 404
        
        attendance_data = get_attendance_data_for_a_unit(attendance_date, unit)

        return jsonify(
            success=True,
            message='Success',
            data=list(map(lambda attendance_record: attendance_record.to_json(), attendance_data))
        ), 200

    def post(self):
        request_body = request.json
        
        student_code = request_body.get('student_code')
        attendance_date_str = request_body.get('attendance_date')
        lesson_status = request_body.get('lesson_status')
        mass_status = request_body.get('mass_status')
        
        try:
            attendance_date = datetime.datetime.strptime(attendance_date_str, '%Y%m%d').date()
        except ValueError:
            return jsonify(
                success=False,
                message='Ngày điểm danh phải ở định dạng YYYYMMDD'
            ), 400
        
        existing_student = get_student_by_student_code(student_code)
        
        if (existing_student is None):
            return jsonify(
                success=False,
                message='Không tìm thấy học viên',
                data=None
            ), 404

        updated_student_attendance = create_or_update_student_attendance(
            existing_student,
            attendance_date,
            AttendanceStatusEnum(mass_status) if mass_status else None,
            AttendanceStatusEnum(lesson_status) if lesson_status else None
        )

        db.session.flush()
        db.session.commit()
        
        return jsonify(
            success=True,
            message='Success',
            data=updated_student_attendance.to_json()
        ), 200

class AttendancesReportHandler(MethodView):
    decorators = [login_required]

    def get(self, unit_id):
        unit = get_unit_by_id(unit_id)

        if (unit is None):
            return jsonify(
                success=False,
                message='Không tìm thấy lớp học',
                data=None
            ), 404
        
        attendance_report_data = get_unit_attendance_report_data(
            datetime.date(2025, 3, 2),
            datetime.date.today(),
            unit
        )

        result_excel_file = export_unit_attendance_report_to_excel(attendance_report_data)

        return send_file(
            result_excel_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='bang-diem-danh-lop-{}.xlsx'.format(unit.unit_id)
        )

attendance_bp.add_url_rule(
    '/attendances',
    view_func=AttendancesHandler.as_view('attendances'),
    methods=['GET', 'POST']
)

attendance_bp.add_url_rule(
    '/attendances/<unit_id>/report',
    view_func=AttendancesReportHandler.as_view('attendances_report'),
    methods=['GET']
)