import re, string, random

from datetime import timedelta

from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..helpers import constants

from ..models.base import db
from ..models.user_account import UserAccount

def __generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    if (any(c.isupper() for c in password) 
        and any(c.islower() for c in password) 
        and any(c.isdigit() for c in password) 
        and any(c in string.punctuation for c in password)):
        return password
    return __generate_strong_password(length)

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

def create_user_account_from_cli(login_id, is_admin=False):
    random_password = __generate_strong_password()
    result, message = create_user_account(login_id, random_password, is_admin)
    if result:
        return True, random_password
    else:
        return False, message

def reset_user_password(user: UserAccount):
    new_password = __generate_strong_password()
    hashed_password = generate_password_hash(
        new_password, method='pbkdf2:sha256', salt_length=8
    )
    user.password = hashed_password
    db.session.flush()
    return True, new_password

def change_user_password(user: UserAccount, old_password, new_password):
    if not check_password_hash(user.password, old_password):
        return False, 'Mật khẩu cũ không đúng'
    
    if len(new_password) < constants.MINIMUM_PASSWORD_LENGTH or len(new_password) > constants.MAXIMUM_PASSWORD_LENGTH:
        return False, 'Mật khẩu mới ít nhất 8 kí tự'
    
    hashed_password = generate_password_hash(
        new_password, method='pbkdf2:sha256', salt_length=8
    )
    user.password = hashed_password
    db.session.flush()
    
    return True, 'Đổi mật khẩu thành công'

def __handle_failed_login_attempt(existing_account: UserAccount):
    existing_account.failed_login_count += 1
    if existing_account.failed_login_count >= constants.MAXIMUM_FAILED_LOGIN_ATTEMPTS:
        existing_account.is_locked = True
    db.session.flush()

def login(login_id, password):
    
    failed_message = 'Đăng nhập thất bại. Vui lòng kiếm tra lại thông tin'
    existing_account = UserAccount.query.filter_by(login_id=login_id).first()
    if existing_account is None:
        return False, failed_message
    if existing_account.is_locked:
        failed_message = 'Tài khoản đã bị khóa do đăng nhập sai quá nhiều lần. Vui lòng liên hệ admin'
        return False, failed_message
    if not check_password_hash(existing_account.password, password):
        __handle_failed_login_attempt(existing_account)
        return False, failed_message
    
    # Call login function here
    login_user(existing_account, remember=True, duration=timedelta(days=constants.REMEMBER_ME_DAYS))
    existing_account.failed_login_count = 0
    db.session.flush()
    
    return True, 'Đăng nhập thành công'

def logout():
    logout_user()
    return True, 'Đăng xuất thành công'