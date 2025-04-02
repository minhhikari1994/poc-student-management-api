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

    @property
    def full_name(self):
        full_name_arr = [self.last_name, self.middle_name, self.first_name]
        return ' '.join(filter(lambda name_seg: name_seg is not None and name_seg.strip() != "", full_name_arr))

    
    def to_json(self):
        return dict(
            id=self.id,
            student_code=self.student_code,
            saint_name=self.saint_name,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            gender=self.gender.name,
            date_of_birth=self.date_of_birth,
            address_one=self.address_one,
            address_two=self.address_two,
        )

    @property
    def qr_code_str(self):
        church_name="Tam Hà"
        student_code=self.student_code
        full_name=self.full_name
        gender= "Nam" if self.gender == StudentGenderEnum.MALE else "Nữ"
        return f"{church_name}|{student_code}|{full_name}|{gender}"


