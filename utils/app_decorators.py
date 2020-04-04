from functools import wraps
from flask import redirect
from flask_login import current_user


def admin_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return redirect('error_403.html')
        return f(*args, **kwargs)

    return decorated_function


def user_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            return redirect('error_403.html')
        return f(*args, **kwargs)

    return decorated_function
