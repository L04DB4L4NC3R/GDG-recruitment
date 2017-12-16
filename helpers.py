from functools import wraps
from flask import url_for,redirect,session


def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not session.get("name"):
            return redirect(url_for('login') )
        return f(*args,**kwargs)
    return decorated_function

