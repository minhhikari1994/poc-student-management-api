from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID

from .base import db

class TestScore(db.Model):
    __tablename__ = "test_scores"
    __table_args__ = (db.PrimaryKeyConstraint("test_id", "student_id"),)

    test_id = db.Column(Integer, db.ForeignKey('tests.id'), nullable=False)
    student_id = db.Column(UUID(as_uuid=True), db.ForeignKey('student.id'), nullable=False)
    score = db.Column(db.Numeric)

    # relation
    student = db.relationship("Student", backref="test_scores")
    test = db.relationship("Test", backref="test_scores")

    def to_json(self):
        return dict(
            test_id=self.test_id,
            student_id=self.student_id,
            score=self.score,
            student=self.student.to_json(),
            test=self.test.to_json()
        )
