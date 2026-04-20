"""Custom route decorators for role-based authorization."""

from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def roles_required(*roles):
    """Restrict route access to users with one of the allowed roles."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Check user role before allowing route execution."""
            if current_user.role not in roles:
                flash("You are not authorized to access this page.", "danger")
                return redirect(url_for("alumni.dashboard"))
            return func(*args, **kwargs)

        return wrapper

    return decorator
