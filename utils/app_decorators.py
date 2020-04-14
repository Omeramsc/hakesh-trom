from functools import wraps
from flask import redirect, abort
from flask_login import current_user


def admin_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def user_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function
