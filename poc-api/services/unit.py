from ..models import Unit

def get_all_units():
    all_units = Unit.query.all()
    return all_units