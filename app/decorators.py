from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash

"""Authorization helpers.

This module provides decorator(s) to restrict access to views based
on the `User.role` value.
"""


# ----------------------------------
# ROLE REQUIRED DECORATOR
# ----------------------------------
# Ensures only users with specific role
# can access certain routes
def role_required(role):

    """Return a decorator that restricts access to users with `role`.

    Usage:
        @login_required
        @role_required("instructor")
        def view():
            ...
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # If user not logged in → redirect to login
            if not current_user.is_authenticated:
                flash("Please login first.")
                return redirect(url_for("auth.login"))

            # If logged in but wrong role → deny access
            if current_user.role != role:
                flash("Access denied!")
                return redirect(url_for("main.home"))

            return func(*args, **kwargs)

        return wrapper

    return decorator