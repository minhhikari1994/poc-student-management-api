from ..models import Student

def get_student_by_student_code(student_code):
    return Student.query.filter_by(student_code=student_code).first()