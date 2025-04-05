import imgkit, segno, click, os, shutil
from flask import Blueprint, render_template, current_app

from ..helpers.enums import StudentGenderEnum
from ..models import Student, StudyYear

from ..services.unit import get_unit_by_id
from ..services.student import get_student_by_student_code

card_gen_cli = Blueprint('card_gen_cli', __name__)

def __render_student_card_front(student: Student):
    qr_string = student.qr_code_str
    print("Generating QR for: {}".format(qr_string))
    qr_code = segno.make(qr_string, version=5)
    student_card_html = render_template(
        'student-card/front.html',
        saint_name=student.saint_name if student.saint_name is not None else '(chưa cập nhật)',
        full_name=student.full_name,
        dob=student.date_of_birth.strftime("%d/%m/%Y") if student.date_of_birth else '(chưa cập nhật)',
        student_code=student.student_code,
        gender="Nam" if student.gender == StudentGenderEnum.MALE else "Nữ",
        qr_svg=qr_code.svg_inline(scale=6)
    )
    return student_card_html

def __render_student_card_back():
    student_card_back_html = render_template(
        'student-card/back.html',
    )
    return student_card_back_html

@card_gen_cli.cli.command('all_units')
@click.argument('study_year')
@click.argument('dest')
def create_student_card_for_all_units(study_year, dest):
    png_config={
        "crop-h": "639",
        "crop-w": "1011",
        "quality": 89
    }
    study_year = StudyYear.query.filter_by(study_year_code=study_year).first()
    if study_year is None:
        print("Không tìm thấy năm học")
        return
    
    all_grades = study_year.grades
    all_units = []
    for grade in all_grades:
        all_units.extend(grade.units)

    for unit in all_units:
        print("=============== Đang xử lý cho lớp: {}==================".format(unit.unit_id))

        if not os.path.exists(f'{dest}/{unit.unit_id}'):
            os.makedirs(f'{dest}/{unit.unit_id}')

        unit_students = unit.students
        for student in unit_students:
            print("Đang xử lý cho học viên: {}".format(student.student_code))
            student_card_front_html = __render_student_card_front(student)
            student_card_back_html = __render_student_card_back()
            imgkit.from_string(student_card_front_html, f'{dest}/{unit.unit_id}/{student.student_code}-side1.png', options=png_config)
            imgkit.from_string(student_card_back_html, f'{dest}/{unit.unit_id}/{student.student_code}-side2.png', options=png_config)
            

@card_gen_cli.cli.command('student')
@click.argument('student_code')
@click.argument('dest')
def create_student_card_for_specific_student(student_code, dest):
    png_config={
        "crop-h": "639",
        "crop-w": "1011",
        "quality": 89
    }
    student = get_student_by_student_code(student_code)
    if student is None:
        print("Không tìm thấy học viên")
        return

    print("Đang xử lý cho học viên: {}".format(student.student_code))

    student_card_front_html = __render_student_card_front(student)
    student_card_back_html = __render_student_card_back()

    imgkit.from_string(student_card_front_html, f'{dest}/{student.student_code}/{student.student_code}-side1.png', options=png_config)
    imgkit.from_string(student_card_back_html, f'{dest}/{student.student_code}/{student.student_code}-side2.png', options=png_config)

@card_gen_cli.cli.command('unit')
@click.argument('unit_id')
@click.argument('dest')
def create_student_card_for_specific_unit(unit_id, dest):
    png_config={
        "crop-h": "639",
        "crop-w": "1011",
        "quality": 89
    }

    chosen_unit = get_unit_by_id(unit_id)
    if chosen_unit is None:
        print("Không tìm thấy lớp học")
        return
    
    if not os.path.exists(f'{dest}/{chosen_unit.unit_id}'):
        os.makedirs(f'{dest}/{chosen_unit.unit_id}')
    
    unit_students = chosen_unit.students
    for student in unit_students:
        print("Đang xử lý cho học viên: {}".format(student.student_code))

        student_card_front_html = __render_student_card_front(student)
        student_card_back_html = __render_student_card_back()

        imgkit.from_string(student_card_front_html, f'{dest}/{chosen_unit.unit_id}/{student.student_code}-side1.png', png_config)
        imgkit.from_string(student_card_back_html, f'{dest}/{chosen_unit.unit_id}/{student.student_code}-side2.png', png_config)
    
