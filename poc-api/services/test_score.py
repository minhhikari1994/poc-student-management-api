from ..models.base import db
from ..models.test_score import TestScore

from .student import get_student_by_student_code

def __generate_student_test_score_data(student, test, test_score_list):
    test_score_record = next((record for record in test_score_list if record.student_id == student.id), None)
    if test_score_record:
        return test_score_record
    else:
        return TestScore(
            test=test,
            student=student,
            score=None
        )

def get_test_score_of_a_unit(test, unit):
    all_students = unit.students
    all_student_ids = list(map(lambda student: student.id, all_students))
    test_score_list = TestScore.query.filter(
        TestScore.test_id == test.id,
        TestScore.student_id.in_(all_student_ids)
    ).all()
    
    return list(map(lambda student: __generate_student_test_score_data(student, test, test_score_list), all_students))

def update_test_score(test, student_scores_dict):
    for student_score in student_scores_dict:
        student_code = student_score.get('student_code')

        existing_student = get_student_by_student_code(student_code)

        existing_test_score = TestScore.query.filter(
            TestScore.test_id == test.id,
            TestScore.student_id == existing_student.id
        ).first()

        if existing_test_score:
            existing_test_score.score=student_score.get('score')
        else:
            new_test_score = TestScore(
                test_id=test.id,
                student_id=existing_student.id,
                score=student_score.get('score') or None
            )
            db.session.add(new_test_score)
        
        db.session.flush()
