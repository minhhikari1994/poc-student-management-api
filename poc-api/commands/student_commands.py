import imgkit, segno, click, os
from flask import Blueprint, render_template

from ..helpers.enums import StudentGenderEnum

from ..services.unit import get_unit_by_id

student_cli_bp = Blueprint('student_cli_bp', __name__)

@student_cli_bp.cli.command('cardgen')
@click.argument('unit_id')
@click.argument('dest')
def create_student_card(unit_id, dest):
    png_config={
        "crop-h": "639",
        "crop-w": "1011"
    }

    chosen_unit = get_unit_by_id(unit_id)
    if chosen_unit is None:
        print("Không tìm thấy lớp học")
        return
    
    if not os.path.exists(f'{dest}/{unit_id}'):
        os.makedirs(f'{dest}/{unit_id}')
    
    unit_students = chosen_unit.students
    print(chosen_unit)
    for student in unit_students:
        print("Đang xử lý cho học viên: {}".format(student.student_code))
        qr_string = student.qr_code_str
        qr_code = segno.make(qr_string, version=5)

        student_card_html = render_template(
            'student-card/index.html',
            saint_name=student.saint_name if student.saint_name is not None else '(chưa cập nhật)',
            full_name=student.full_name,
            dob=student.date_of_birth.strftime("%d/%m/%Y") if student.date_of_birth else '(chưa cập nhật)',
            student_code=student.student_code,
            gender="Nam" if student.gender == StudentGenderEnum.MALE else "Nữ",
            qr_svg=qr_code.svg_inline(scale=6)
        )

        imgkit.from_string(student_card_html, f'{dest}/{unit_id}/{student.student_code}.png', png_config)
    
