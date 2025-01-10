from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID

from .base import db

class Unit(db.Model):
    id = db.Column(Integer, primary_key=True)
    unit_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    grade_id = db.Column(Integer, db.ForeignKey('grade.id'), nullable=False)