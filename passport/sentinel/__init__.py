from datetime import datetime
from functools import wraps
import json

from flask import abort, request
from jose.constants import ALGORITHMS
from jose.exceptions import JWSError
from jose import jws
import requests

from .extensions import store


class Authorizer(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.log = app.logger
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['jwt.authenticator'] = self

    def require_token(self):
        """Protect resource with oauth/auth/jwt token."""
        def wrapper(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                if not self.app.config.get('SENTINEL_PROTECTED', False):
                    return f(*args, **kwargs)

                secret_key = self.app.config.get('SECRET_KEY', None)
                token_type, auth_token = self.get_token()
                if not auth_token:
                    self.log.info('Missing oauth token')
                    abort(401)
                if (token_type == 'auth-token' and auth_token != secret_key):
                    self.log.info('invalid token')
                    abort(401)
                if token_type == 'oauth':
                    is_valid, user_data = self.validate_oauth_token(auth_token)
                    if not is_valid:
                        abort(401)
                    request.user = json.loads(user_data)
                return f(*args, **kwargs)
            return decorated
        return wrapper

    def authorize(self, response):
        private_key = Authorizer.read_key(
            self.app.config['SENTINEL_JWT_PRIVATE_KEY'])
        algorithm = getattr(
            ALGORITHMS, self.app.config['SENTINEL_JWT_ALGORITHM'])
        return jws.sign(
            response, private_key, algorithm=algorithm)

    def verify_jwt(self, jwt, auth_token=None):
        try:
            secret_key = Authorizer.read_key(
                self.app.config['SENTINEL_JWT_PUBLIC_KEY'])
            response_data = json.loads(jws.verify(
                jwt, secret_key, ALGORITHMS.RS256))
        except JWSError:
            if auth_token:
                headers = {'Authorization': auth_token}
                response = requests.get(self.app.config['PASSPORT_BASE_URL'],
                                        headers=headers)
                response_data = response.json()['user']
            else:
                raise
        return response_data

    def validate_oauth_token(self, auth_token):
        is_valid_token = True
        user_data = None
        if auth_token in store.keys():
            oauth_data = json.loads(store.get(auth_token))
            if Authorizer.validate_token_expiration_date(
                    oauth_data['expires']):
                self.log.info('Expired token')
                is_valid_token = False
            else:
                user_data = self.verify_jwt(oauth_data['jwt'], auth_token)
        else:
            self.log.info('invalid token')
            is_valid_token = False
        return (is_valid_token, user_data)

    @staticmethod
    def get_token():
        """Return the token associated with the request
        Check the token type (jwt/oauth/auth) and perform necessary steps
        if token type is oauth, else return the token itself
        """
        token_type = 'no-token'
        auth_token = None
        if 'authorization-token' in request.headers:
            auth_token = request.headers.get('authorization-token')
            token_type = 'auth-token'
        elif 'Authorization' in request.headers:
            auth_token = request.headers.get('Authorization', None)
            token_type = 'jwt'
            if auth_token.startswith('Bearer '):
                auth_token = auth_token[7:]
                token_type = 'oauth'
        return (token_type, auth_token)

    @staticmethod
    def validate_token_expiration_date(expires):
        is_expired = False
        token_expiration_date = datetime.strptime(
            expires, '%Y-%m-%d %H:%M:%S.%f')
        if token_expiration_date < datetime.now():
            is_expired = True
        return is_expired

    @staticmethod
    def read_key(key):
        secret_key = None
        with open(key, 'rb') as key_file:
            secret_key = key_file.read()

        return secret_key
