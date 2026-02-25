from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please login first.")
                return redirect(url_for("auth.login"))

            if current_user.role != role:
                flash("Access denied!")
                return redirect(url_for("main.home"))

            return func(*args, **kwargs)
        return wrapper
    return decorator