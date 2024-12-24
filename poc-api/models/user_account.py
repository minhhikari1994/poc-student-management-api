from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from flask_login import UserMixin

from .base import db

class UserAccount(db.Model, UserMixin):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=db.func.gen_random_uuid()
    )
    login_id = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False, server_default="false", nullable=False)