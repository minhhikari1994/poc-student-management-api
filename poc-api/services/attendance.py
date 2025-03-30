import datetime

from ..models.base import db
from ..models import StudentAttendance, Unit, Student

from ..helpers.enums import AttendanceStatusEnum

def __generate_student_attendance_data(student: Student, attendance_date: datetime, attendance_list: list):
    attendance_record = next((record for record in attendance_list if record.student_id == student.id), None)
    if attendance_record:
        return attendance_record
    else:
        return StudentAttendance(
            student=student,
            attendance_date=attendance_date,
            mass_status=AttendanceStatusEnum.ABSENT,
            lesson_status=AttendanceStatusEnum.ABSENT,
        )

def get_attendance_data_for_a_unit(attendance_date, unit: Unit):
    unit_students = unit.students;
    all_student_ids = list(map(lambda student: student.id, unit_students))
    attendance_list = StudentAttendance.query.filter(
        StudentAttendance.attendance_date == attendance_date,
        StudentAttendance.student_id.in_(all_student_ids)
    ).all()
    return list(map(lambda student: __generate_student_attendance_data(student, attendance_date, attendance_list), unit_students))
    
def create_or_update_student_attendance(student: Student, attendance_date: datetime, mass_status, lesson_status):
    student_attendance = StudentAttendance.query.filter(
        StudentAttendance.student_id == student.id,
        StudentAttendance.attendance_date == attendance_date
    ).first()
    if student_attendance:
        student_attendance.mass_status = mass_status
        student_attendance.lesson_status = lesson_status
        db.session.flush()
    else:
        student_attendance = StudentAttendance(
            student=student,
            attendance_date=attendance_date,
            mass_status=mass_status,
            lesson_status=lesson_status
        )
        db.session.add(student_attendance)
        db.session.flush()
        
    return student_attendance

def __get_all_sundays_in_time_frame(start_date, end_date):
    sundays = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 6:  # 6 corresponds to Sunday
            sundays.append(current_date)
        current_date += datetime.timedelta(days=1)
    return sundays


def get_unit_attendance_report_data(start_date, end_date, unit: Unit):
    result = dict(
        unit_id=unit.unit_id,
        unit_name=unit.name,
        sundays=__get_all_sundays_in_time_frame(start_date, end_date),
        attendance_data=[]
    )
    unit_students = unit.students;
    all_student_ids = list(map(lambda student: student.id, unit_students))
    attendance_list = StudentAttendance.query.filter(
        StudentAttendance.attendance_date.between(start_date, end_date),
        StudentAttendance.student_id.in_(all_student_ids)
    ).all()

    for student in unit.students:
        all_attendance_of_students = filter(
            lambda att: att.student_id == student.id, attendance_list
        )
        student_attendance_entry = dict(
            student_code=student.student_code,
            saint_name=student.saint_name,
            first_name=student.first_name,
            middle_name=student.middle_name,
            last_name=student.last_name,
            attendances=list(map(lambda att: dict(
                attendance_date=att.attendance_date,
                mass_status=att.mass_status.value if att.mass_status else AttendanceStatusEnum.ABSENT.value,
                lesson_status=att.lesson_status.value if att.lesson_status else AttendanceStatusEnum.ABSENT.value
            ), all_attendance_of_students))
        )
        result.get('attendance_data').append(student_attendance_entry)
        
    return result
    
def get_attendance_data_of_a_student(student: Student, start_date, end_date):
    result = dict(
        total_present_mass=0,
        total_present_lesson=0,
        total_absent_mass=0,
        total_absent_lesson=0,
        attendance_data=[]
    )
    all_sundays = __get_all_sundays_in_time_frame(start_date, end_date)
    student_attendance_list = StudentAttendance.query.filter(
        StudentAttendance.student_id == student.id,
        StudentAttendance.attendance_date.between(start_date, end_date)
    ).all()

    for sunday in all_sundays:
        student_attendance_entry = next((att for att in student_attendance_list if att.attendance_date == sunday), None)
        if (student_attendance_entry is not None):
            attendance_entry = dict(
                attendance_date=sunday,
                mass_status=student_attendance_entry.mass_status.value if student_attendance_entry.mass_status else AttendanceStatusEnum.ABSENT.value,
                lesson_status=student_attendance_entry.lesson_status.value if student_attendance_entry.lesson_status else AttendanceStatusEnum.ABSENT.value
            )
            result.get('attendance_data').append(attendance_entry)
            if student_attendance_entry.mass_status == AttendanceStatusEnum.PRESENT:
                result['total_present_mass'] += 1
            else:
                result['total_absent_mass'] += 1
            if student_attendance_entry.lesson_status == AttendanceStatusEnum.PRESENT:
                result['total_present_lesson'] += 1                
            else:
                result['total_absent_lesson'] += 1
        else:
            result.get('attendance_data').append(dict(
                attendance_date=sunday,
                mass_status=AttendanceStatusEnum.ABSENT.value,
                lesson_status=AttendanceStatusEnum.ABSENT.value
            ))
            result['total_absent_mass'] += 1
            result['total_absent_lesson'] += 1
    
    return result
    
    # for sunday in all_sundays:
    #     student_attendance_entry = next((att for att in student_attendance_list if att.attendance_date == sunday), None)
    #     if (student_attendance_entry is not None):
    #         result.get('attendance_data').append(dict(
    #             attendance_date=sunday,
    #             mass_status=student_attendance_entry.mass_status.value if student_attendance_entry.mass_status else None,
    #             lesson_status=student_attendance_entry.lesson_status.value if student_attendance_entry.lesson_status else None
    #         ))
    #         if (student_attendance_entry.mass_status == AttendanceStatusEnum.Present):