""" Defines decorators to extend other functions """

from functools import wraps
from settings import Config
from flask import request
from flask import make_response


def validate_user(username, password):
    """ Checks username matches password """
    return username == Config.USERNAME and password == Config.PASSWORD


def authenticate(func):
    """ Authenticates user """
    @wraps(func)
    def decorated(*args, **kwargs):
        """ Uses auth headers to validate user """
        auth = request.authorization
        if not auth or not validate_user(auth.username, auth.password):
            response = make_response("", 401)
            response.headers["WWW-Authenticate"] = 'Basic realm="Login Required"'
            return response
        return func(*args, **kwargs)
    return decorated
