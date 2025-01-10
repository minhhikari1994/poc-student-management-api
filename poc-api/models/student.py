from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from .base import db

from ..helpers.enums import StudentGenderEnum

class Student(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=db.func.gen_random_uuid()
    )
    student_code = db.Column(db.String(20), unique=True, nullable=False)
    saint_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.Enum(StudentGenderEnum), nullable=False)
    date_of_birth = db.Column(db.Date())
    address_one = db.Column(db.String(100))
    address_two = db.Column(db.String(100))