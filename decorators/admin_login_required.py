from functools import wraps
from flask import redirect, url_for, session, flash


def admin_login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "admin_logged_in" in session:
            return function(*args, **kwargs)
        else:
            flash("Bu Sayfayı Görmeye Yetkili Değilsiniz.", "danger")
            return redirect(url_for('admin'))

    return decorated_function
