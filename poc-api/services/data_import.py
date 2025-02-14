from datetime import datetime
from pandas import read_excel, isna, NA, ExcelFile

from ..helpers.enums import StudentGenderEnum

from ..models.base import db
from ..models import StudyYear, Grade, Student, Unit, StudentUnit

def __get_middle_name(first_name_from_excel):
    return ' '.join(first_name_from_excel.split(' ')[1:]) if first_name_from_excel else None

def __get_gender(gender_name_from_excel):
    return StudentGenderEnum.MALE if gender_name_from_excel == 'Nam' else StudentGenderEnum.FEMALE

def __get_date_of_birth(date_of_birth_from_excel):
    return datetime.strptime(date_of_birth_from_excel, "%d/%m/%Y").date() if date_of_birth_from_excel else None

def import_student_data(excel_file, sheet_name , unit_code):
    student_df = read_excel(
        excel_file,
        sheet_name=sheet_name,
        header=3,
        dtype="string",
    )

    study_year_code = unit_code.split('-')[0]

    existing_study_year = StudyYear.query.filter_by(study_year_code=study_year_code).first()

    student_df = student_df.replace({NA: None})
    student_dict_from_excel = student_df.to_dict(orient='records')
    student_list = []

    for student in student_dict_from_excel:
        new_student = Student(
            student_code="{study_year_code}-HV{student_code:04}".format(
                study_year_code=existing_study_year.study_year_code,
                student_code=int(student.get('ID'))
            ),
            saint_name=student.get('Tên Thánh'),
            first_name=student.get('Tên'),
            middle_name=__get_middle_name(student.get('Họ')),
            last_name=student.get('Họ').split(' ')[0],
            gender=__get_gender(student.get('Giới Tính')),
            date_of_birth=__get_date_of_birth(student.get('Ngày Sinh').strip()) if student.get('Ngày Sinh') else None,
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

def __import_study_year(excel_file, sheet_name):
    study_year_df = read_excel(
        excel_file,
        sheet_name=sheet_name,
        usecols="A:B",
        header=2,
        dtype="string"
    )
    study_year_df = study_year_df.replace({NA: None})
    study_year_from_excel = study_year_df.to_dict(orient='records')

    for study_year in study_year_from_excel:
        if study_year.get('ID Năm Học') is None:
            continue
        new_study_year = StudyYear(
            study_year_code=study_year.get('ID Năm Học'),
            name=study_year.get('Tên Năm Học'),
            description=study_year.get('Tên Năm Học')
        )
        db.session.add(new_study_year)
    
    db.session.flush()

def __import_grade(excel_file, sheet_name):
    grade_df = read_excel(
        excel_file,
        sheet_name=sheet_name,
        usecols="E:G",
        header=2,
        dtype="string",
    )
    grade_df = grade_df.replace({NA: None})
    grade_from_excel = grade_df.to_dict(orient='records')

    for grade in grade_from_excel:
        if grade.get('ID Năm Học.1') is None:
            continue

        existing_study_year = StudyYear.query.filter_by(study_year_code=grade.get('ID Năm Học.1')).first()

        new_grade = Grade(
            grade_code="{}-{}".format(existing_study_year.study_year_code, grade.get('ID Khối')),
            name=grade.get('Tên Khối'),
            study_year_id=existing_study_year.id
        )
        db.session.add(new_grade)
    
    db.session.flush()

def __import_unit(excel_file, sheet_name):
    unit_df = read_excel(
        excel_file,
        sheet_name=sheet_name,
        usecols="J:M",
        header=2,
        dtype="string",
    )
    unit_df = unit_df.replace({NA: None})
    units_from_excel = unit_df.to_dict(orient='records')

    for unit in units_from_excel:
        existing_study_year = StudyYear.query.filter_by(study_year_code=unit.get('ID Năm Học.2')).first()
        existing_grade = Grade.query.filter_by(grade_code='{}-{}'.format(
            existing_study_year.study_year_code,
            unit.get('ID Khối.1')
        )).first()

        new_unit = Unit(
            unit_id='{}-{}'.format(
                existing_grade.grade_code,
                unit.get('ID Lớp')
            ),
            name=unit.get('Tên Lớp'),
            grade_id=existing_grade.id,
        )
        db.session.add(new_unit)
    
    db.session.flush()

def import_master_data_from_excel(excel_file):
    xl = ExcelFile(excel_file)
    wb = xl.book
    sheet_names = xl.sheet_names
    
    for sheet_name in sheet_names:
        sh = wb[sheet_name]
        
        data_type = sh["B1"]

        if data_type.value == "MASTER":
            __import_study_year(excel_file, sheet_name)
            __import_grade(excel_file, sheet_name)
            __import_unit(excel_file, sheet_name)
        elif data_type.value == "STUDENT_LIST":
            unit_code = sh["B2"].value
            import_student_data(excel_file, sheet_name, unit_code)
    
    db.session.commit()

    return True

