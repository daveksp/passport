from functools import wraps
from flask import abort, request

from jose.constants import ALGORITHMS
from jose.exceptions import JWSError
from jose import jws


class JWTAuthenticator(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['jwt.authenticator'] = self

    def validate_token(self, token):
        secret_key = JWTAuthenticator.read_key(
            self.app.config['JWT_PUBLIC_KEY'])
        payload = jws.verify(
            token, secret_key, ALGORITHMS.RS256)
        return payload

    def require_token(self):
        """Protect resource with specified roles."""
        def wrapper(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                try:
                    authorization_token = request.headers.get('Authorization', "")
                    request.authorization = self.validate_token(authorization_token)
                except JWSError as exc:
                    return abort(401)
                return f(*args, **kwargs)
            return decorated
        return wrapper

    def sign_token(self, response):
        private_key = JWTAuthenticator.read_key(
            self.app.config['JWT_PRIVATE_KEY'])
        algorithm = getattr(ALGORITHMS, self.app.config['JWT_ALGORITHM'])
        return jws.sign(
            response, private_key, algorithm=algorithm)

    @staticmethod
    def read_key(key):
        secret_key = None
        with open(key, 'rb') as key_file:
            secret_key = key_file.read()

        return secret_key
