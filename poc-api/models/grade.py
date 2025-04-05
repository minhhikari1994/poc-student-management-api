from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID

from .base import db

class Grade(db.Model):
    id = db.Column(Integer, primary_key=True)
    grade_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    study_year_id = db.Column(Integer, db.ForeignKey('study_year.id'), nullable=False)
    
    # relation
    units = db.relationship('Unit', backref='grade')
