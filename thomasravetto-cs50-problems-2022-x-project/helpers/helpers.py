import os
from urllib import request
import requests

from flask import redirect, render_template, request, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def check_url(pl_input):
    if len(pl_input) > 34:
        if pl_input[-35] == "=":
            return pl_input[-34:]
        return 1

    elif len(pl_input) == 34:
        if "=" not in pl_input:
            return pl_input
        return 1

    elif len(pl_input) < 34:
        return 1