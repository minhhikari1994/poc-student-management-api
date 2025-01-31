import enum

class StudentGenderEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'

class AttendanceStatusEnum(enum.Enum):
    PRESENT = 'present'
    NOTIFIED_ABSENT = 'notified_absent'
    ABSENT = 'absent'

class SemesterEnum(enum.Enum):
    FIRST_SEMESTER = 'first_semester'
    SECOND_SEMESTER = 'second_semester'