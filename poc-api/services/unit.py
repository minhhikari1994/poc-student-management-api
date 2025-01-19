from ..models import Unit, Result

def get_all_units():
    all_units = Unit.query.all()
    return all_units

def get_unit_by_id(unit_id):
    unit = Unit.query.filter_by(unit_id=unit_id).first()
    return unit
    