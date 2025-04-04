from ..models.base import db
from ..models import TestScore, Grade

from .student import get_student_by_student_code
from .test import get_test_list_for_a_grade

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

def get_test_score_of_a_student_in_a_grade(student, grade_code):
    student_grade = Grade.query.filter_by(grade_code=grade_code).first()
    grade_test_list = get_test_list_for_a_grade(student_grade)

    grade_test_ids = list(map(lambda test: test.id, grade_test_list))

    student_test_score_list = TestScore.query.filter(
        TestScore.test_id.in_(grade_test_ids),
        TestScore.student_id == student.id
    ).all()

    result = []
    for grade_test in grade_test_list:
        test_score_record = next((record for record in student_test_score_list if record.test_id == grade_test.id), None)
        if test_score_record:
            result.append(
                dict(
                    test_id=grade_test.id,
                    test_name=grade_test.name,
                    score=test_score_record.score
                )
            )
        else:
            result.append(
                dict(
                    test_name=grade_test.name,
                    score=None
                )
            )
    return result

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
