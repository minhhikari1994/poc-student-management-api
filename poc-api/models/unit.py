from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID

from .base import db

class Unit(db.Model):
    id = db.Column(Integer, primary_key=True)
    unit_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    grade_id = db.Column(Integer, db.ForeignKey('grade.id'), nullable=False)

    # relation
    grade = db.relationship('Grade', foreign_keys=[grade_id])
    students = db.relationship('Student', secondary='student_unit')

    def to_json(self):
        return dict(
            id=self.id,
            unit_id=self.unit_id,
            name=self.name,
            grade_id=self.grade_id,
            grade_name=self.grade.name
        )
