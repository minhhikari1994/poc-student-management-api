from datetime import datetime
from pandas import read_excel, isna, NA

from ..helpers.enums import StudentGenderEnum

from ..models.base import db
from ..models import Student, Unit, StudentUnit

def __get_middle_name(first_name_from_excel):
    return ' '.join(first_name_from_excel.split(' ')[1:]) if first_name_from_excel else None

def __get_gender(gender_name_from_excel):
    return StudentGenderEnum.MALE if gender_name_from_excel == '1 Nam' else StudentGenderEnum.FEMALE

def __get_date_of_birth(date_of_birth_from_excel):
    return datetime.strptime(date_of_birth_from_excel, "%d/%m/%Y").date() if date_of_birth_from_excel else None

def import_student_data(student_excel_file, study_year_code, unit_code):
    student_df = read_excel(
        student_excel_file,
        sheet_name='2024VD1B',
        header=7,
        dtype="string",
    )
    student_df = student_df.replace({NA: None})
    student_dict_from_excel = student_df.to_dict(orient='records')
    student_list = []

    for student in student_dict_from_excel:
        new_student = Student(
            student_code="{study_year_code}-HV{student_code:04}".format(
                study_year_code=study_year_code,
                student_code=int(student.get('STT'))
            ),
            saint_name=student.get('Tên Thánh'),
            first_name=student.get('Tên'),
            middle_name=__get_middle_name(student.get('Họ')),
            last_name=student.get('Họ').split(' ')[0],
            gender=__get_gender(student.get('Giới Tính')),
            date_of_birth=__get_date_of_birth(student.get('Ngày sinh').strip()) if student.get('Ngày sinh') else None,
            address_one=None,
            address_two=None
        )
        student_list.append(new_student)

    db.session.add_all(student_list)
    db.session.flush()

    unit = Unit.query.filter_by(unit_id=unit_code).first()

    for student in student_list:
        student_unit = StudentUnit(
            student_id=student.id,
            unit_id=unit.id
        )
        db.session.add(student_unit)
    db.session.flush()

    db.session.commit()
    return student_list