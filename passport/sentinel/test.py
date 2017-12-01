from unittest import TestCase

from freezegun import freeze_time
from nose.tools import eq_
from mock import patch, mock_open
from werkzeug.exceptions import Unauthorized

from passport import create_app
from . import Authorizer


class SentinelTests(TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.authorizer = Authorizer(self.app)

    def test_read_key(self):
        with patch("__builtin__.open", mock_open(read_data="secret_key")):
            secret_key = Authorizer.read_key('test_key')
            eq_(secret_key, 'secret_key')

    @patch('passport.sentinel.request')
    def test_get_token_auth_type(self, mock_request):
        mock_request.headers = {"authorization-token": "secret"}
        with self.app.test_request_context('/?name=Peter'):
            (token_type, auth_token) = Authorizer.get_token()
            eq_(token_type, "auth-token")
            eq_(auth_token, "secret")

    @patch('passport.sentinel.request')
    def test_get_token_oauth_type(self, mock_request):
        mock_request.headers = {"Authorization": "Bearer secret"}
        with self.app.test_request_context('/?name=Peter'):
            (token_type, auth_token) = Authorizer.get_token()
            eq_(token_type, "oauth")
            eq_(auth_token, "secret")

    @patch('passport.sentinel.request')
    def test_get_token_jwt_type(self, mock_request):
        mock_request.headers = {"Authorization": "secret"}
        with self.app.test_request_context('/?name=Peter'):
            (token_type, auth_token) = Authorizer.get_token()
            eq_(token_type, "jwt")
            eq_(auth_token, "secret")

    @freeze_time('2017-06-28 12:01')
    def test_validate_token_expiration_date(self):
        is_expired = Authorizer.validate_token_expiration_date(
            '2017-11-26 06:24:25.546749')
        with self.app.test_request_context('/?name=Peter'):
            eq_(is_expired, False)

    @freeze_time('2017-06-28 12:01')
    def test_validate_token_expiration_date_failure(self):
        is_expired = Authorizer.validate_token_expiration_date(
            '2017-06-25 06:24:25.546749')
        with self.app.test_request_context('/?name=Peter'):
            eq_(is_expired, True)

    @freeze_time('2017-06-28 12:01')
    @patch('passport.sentinel.Authorizer.verify_jwt')
    @patch('passport.sentinel.store')
    @patch('passport.sentinel.request')
    def test_validate_oauth_token(self, mock_request, mock_store, mock_jwt):
        expected_user_data = {"username": "test user", "email": "test@email.com"}
        mock_store.keys.return_value = {'secret', 'other-secret'}
        mock_store.get.return_value = '{"jwt": "aaaa.bbbb.cccc", "expires":"2017-11-26 06:24:25.546749"}'
        mock_jwt.return_value = expected_user_data
        with self.app.test_request_context('/?name=Peter'):
            is_valid_token, user_data = self.authorizer.validate_oauth_token('secret')
            eq_(is_valid_token, True)
            eq_(user_data, expected_user_data)

    @patch('passport.sentinel.store')
    def test_validate_oauth_token_invalid_token(self, mock_store):
        mock_store.keys.return_value = {'other-secret'}
        with self.app.test_request_context('/?name=Peter'):
            is_valid_token, user_Data = self.authorizer.validate_oauth_token('secret')
            eq_(is_valid_token, False)
            eq_(user_Data, None)

    @freeze_time('2017-06-28 12:01')
    @patch('passport.sentinel.store')
    def test_validate_oauth_token_expired_token(self, mock_store):
        mock_store.keys.return_value = {'secret', 'other-secret'}
        mock_store.get.return_value = '{"user": "Test User", "expires":"2017-06-25 06:24:25.546749"}'
        with self.app.test_request_context('/?name=Peter'):
            is_valid_token, user_Data = self.authorizer.validate_oauth_token('secret')
            eq_(is_valid_token, False)
            eq_(user_Data, None)

    def test_verify_jwt(self):
        expected_user_data = {"username": "test user", "email": "test@email.com"}
        jwt = self.authorizer.authorize(expected_user_data)
        with self.app.test_request_context('/?name=Peter'):
            response_data = self.authorizer.verify_jwt(jwt, "secret")
            eq_(response_data, expected_user_data)

    @patch('passport.sentinel.Authorizer.validate_oauth_token')
    @patch('passport.sentinel.request')
    def test_require_token(self, mock_request, mock_token_validator):
        expected_user_data = '{"username": "test user", "email": "test@email.com"}'
        mock_request.headers = {"Authorization": "Bearer correct_token"}
        mock_token_validator.return_value = (True, expected_user_data)

        @self.authorizer.require_token()
        def decorated_func():
            return 'test'

        with self.app.test_request_context('/?name=Peter'):
            result = decorated_func()
            eq_(result, 'test')

    def test_require_token_disabled_protection(self):
        self.app.config['SENTINEL_PROTECTED'] = False

        @self.authorizer.require_token()
        def decorated_func():
            return 'test'

        with self.app.test_request_context('/?name=Peter'):
            result = decorated_func()
            eq_(result, 'test')

    def test_require_token_missing_token(self):

        @self.authorizer.require_token()
        def decorated_func():
            return 'test'

        with self.app.test_request_context('/?name=Peter'),\
             self.assertRaises(Unauthorized):
            decorated_func()

    @patch('passport.sentinel.request')
    def test_require_token_invalid_auth_token(self, mock_request):
        mock_request.headers = {"authorization-token": "other-secret"}

        @self.authorizer.require_token()
        def decorated_func():
            return 'test'
        
        with self.app.test_request_context('/?name=Peter'),\
             self.assertRaises(Unauthorized):
            decorated_func()

    @patch('passport.sentinel.request')
    def test_require_token_valid_auth_token(self, mock_request):
        mock_request.headers = {"authorization-token": "SECRET"}

        @self.authorizer.require_token()
        def decorated_func():
            return 'test'
        
        with self.app.test_request_context('/?name=Peter'):
            result = decorated_func()
            eq_(result, 'test')

    @patch('passport.sentinel.request')
    def test_require_token_invalid_oauth_token(self, mock_request):
        mock_request.headers = {"Authorization": "Bearer wrong_token"}
        
        @self.authorizer.require_token()
        def decorated_func():
            return 'test'
        
        with self.app.test_request_context('/?name=Peter'),\
             self.assertRaises(Unauthorized):
            decorated_func()

