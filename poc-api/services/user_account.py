import re

from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..helpers import constants

from ..models.base import db
from ..models.user_account import UserAccount

def create_user_account(login_id, password, is_admin=False):
    if re.match(constants.VALID_EMAIL_REGEX, login_id) is None:
        return False, 'Login id must be a valid email address'
    if len(password) < constants.MINIMUM_PASSWORD_LENGTH or len(password) > constants.MAXIMUM_PASSWORD_LENGTH:
        return False, 'Password must be between 8 and 32 characters'
    
    existing_account = UserAccount.query.filter_by(login_id=login_id).first()
    if existing_account is not None:
        return False, 'Login id already exists'
    
    hashed_password = generate_password_hash(
        password, method='pbkdf2:sha256', salt_length=8
    )
    
    user_account = UserAccount(login_id=login_id, password=hashed_password, is_admin=is_admin)
    db.session.add(user_account)
    db.session.flush()
    
    return True, 'Account created successfully'

def login(login_id, password):
    
    failed_message = 'Login failed'
    existing_account = UserAccount.query.filter_by(login_id=login_id).first()
    if existing_account is None:
        return False, failed_message
    if not check_password_hash(existing_account.password, password):
        return False, failed_message
    
    # Call login function here
    login_user(existing_account)
    return True, 'Login success'

def logout():
    logout_user()
    return True, 'Logout success'