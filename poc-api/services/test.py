from ..models import Test

def get_test(test_id):
    test = Test.query.get(test_id)
    return test

def get_test_list_for_a_unit(unit):
    grade_id = unit.grade.id
    test_list = Test.query.filter_by(grade_id=grade_id).all()
    return test_list

def get_test_list_for_a_grade(grade):
    grade_id = grade.id
    test_list = Test.query.filter_by(grade_id=grade_id).all()
    return test_list