from ..models import Unit, Result

def get_all_units():
    all_units = Unit.query.all()
    return all_units

def get_student_list_in_a_unit(unit_id):
    unit = Unit.query.filter_by(unit_id=unit_id).first()
    if (unit is None):
        return Result.error('Không tìm thấy lớp học')
    return Result.success('Success', unit.students)
    