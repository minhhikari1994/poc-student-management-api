import datetime

from ..models.base import db
from ..models import StudentAttendance, Unit, Student

def __generate_student_attendance_data(student: Student, attendance_date: datetime, attendance_list: list):
    attendance_record = next((record for record in attendance_list if record.student_id == student.id), None)
    if attendance_record:
        return attendance_record
    else:
        return StudentAttendance(
            student=student,
            attendance_date=attendance_date,
            mass_status=None,
            lesson_status=None,
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
