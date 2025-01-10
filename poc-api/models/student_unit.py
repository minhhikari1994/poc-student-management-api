from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID

from .base import db

class StudentTrainingCourse(db.Model):
    __tablename__ = "student_unit"
    __table_args__ = (db.PrimaryKeyConstraint("student_id", "unit_id"),)

    student_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("student.id"), nullable=False
    )
    unit_id = db.Column(
        Integer, db.ForeignKey("unit.id"), nullable=False
    )