from functools import wraps
from flask import jsonify

from flask_login import current_user

def admin_required(f):
    """
    This decorator checks if the user is an admin before allowing them to
    access the decorated function. If the user is not an admin, it returns
    a 403 error.

    :param f: function to be decorated
    :return: The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user or not current_user.is_admin:
            return jsonify(success=False, message='You are not allowed to perform this action'), 403
        return f(*args, **kwargs)
    return decorated_function
