from sqlalchemy import Integer, Text
from sqlalchemy.dialects.postgresql import UUID

from .base import db

class StudyYear(db.Model):
    id = db.Column(Integer, primary_key=True)
    study_year_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(Text, nullable=False)

    # relation
    grades = db.relationship('Grade', backref='study_year')