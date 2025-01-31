from sqlalchemy import Integer
from ..helpers.enums import SemesterEnum

from .base import db

class Test(db.Model):
    __tablename__ = "tests"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    factor = db.Column(Integer, nullable=False)
    semester = db.Column(db.Enum(SemesterEnum), nullable=False)
    grade_id = db.Column(Integer, db.ForeignKey('grade.id'), nullable=False)

    def to_json(self):
        return dict(
            id=self.id,
            name=self.name,
            factor=self.factor,
            semester=self.semester.value,
        )
