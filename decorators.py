""" Defines decorators to extend other functions """

import hashlib
from functools import wraps
from settings import Config
from flask import request
from flask import make_response


TOKEN = hashlib.sha256(Config.UNIQUE_TOKEN).hexdigest()
TOKEN_HEADER_NAME = "MY_AUTH_TOKEN"


def validate_user(username, password):
    """ Checks username matches password """
    return username == Config.USERNAME and password == Config.PASSWORD


def authenticate(is_user_valid_function):
    """ Authenticates user """
    def auth(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            """ Uses auth headers to validate user """
            auth = request.authorization
            if not auth or not is_user_valid_function(auth.username, auth.password):
                response = make_response("", 401)
                response.headers["WWW-Authenticate"] = 'Basic realm="Login Required"'
                return response
            kwargs[TOKEN_HEADER_NAME] = TOKEN
            return func(*args, **kwargs)
        return decorated
    return auth


def check_token(func):
    """ Checks token in request """
    @wraps(func)
    def decorated(*args, **kwargs):
        if request.headers[TOKEN_HEADER_NAME] and request.headers[TOKEN_HEADER_NAME] != TOKEN:
            response = make_response("", 401)
            response.headers["X-APP-ERROR-CODE"] = 9500
            response.headers["X-APP-ERROR-MESSAGE"] = "No valid authentication found in request"
            return response
        return func(*args, **kwargs)
    return decorated
