from .base import db
from sqlalchemy.dialects.postgresql import UUID

from ..helpers.enums import AttendanceStatusEnum

class StudentAttendance(db.Model):
    __tablename__ = "student_attendance"
    __table_args__ = (db.PrimaryKeyConstraint("student_id", "attendance_date"),)

    student_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("student.id"), nullable=False
        )    
    attendance_date = db.Column(db.Date(), nullable=False)
    mass_status = db.Column(db.Enum(AttendanceStatusEnum))
    lesson_status = db.Column(db.Enum(AttendanceStatusEnum))

    # reationship
    student = db.relationship("Student", backref="student_attendances")

    def to_json(self):
        return dict(
            student=self.student.to_json(),
            attendance_date=self.attendance_date,
            mass_status=self.mass_status.value if self.mass_status else AttendanceStatusEnum.ABSENT.value,
            lesson_status=self.lesson_status.value if self.lesson_status else AttendanceStatusEnum.ABSENT.value
        )


