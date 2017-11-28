from unittest import TestCase

from nose.tools import eq_
from mock import patch, mock_open

from passport import create_app
from passport.api.exceptions import (ApiException, AccountException,
                                     RequestDataException)
from passport.api.common.failures import Failures as CommonFailures
from passport.api.users.failures import Failures
from passport.api.users.schema import UserSchema
from passport.models import User

from ...mocks.common import user_data


class SchemaTests(TestCase):

    def setUp(self):
        self.app = create_app(settings_override={
            'SQLALCHEMY_DATABASE_URI': "sqlite://"
        })
        self.app.config['TESTING'] = True

    @patch('passport.api.users.schema.db')
    @patch('passport.api.users.schema.User')
    def test_user_load(self, mock_user, mock_db):
        schema = UserSchema()
        user_json = user_data(json=False)
        mock_user.query.filter.return_value.first.return_value = None
        mock_db.or_.return_value = 'test'
        with self.app.app_context():
            response_object, errors = schema.load(user_json)

    def test_user_load_empty_password(self):
        schema = UserSchema()
        user_json = user_data(json=False)
        user_json['password'] = ''
        with self.app.app_context(), self.assertRaises(RequestDataException) as error_context:
            schema.validate_passwords(user_json)
        eq_(error_context.exception.errors, Failures.empty_password)

    def test_user_load_passwords_doesnt_match(self):
        schema = UserSchema()
        user_json = user_data(json=False)
        user_json['password'] = 'abcdefgh'
        with self.app.app_context(), self.assertRaises(RequestDataException) as error_context:
            schema.validate_passwords(user_json)
        eq_(error_context.exception.errors, Failures.passwords_doesnt_match)

    def test_user_load_passwords_too_week(self):
        schema = UserSchema()
        user_json = user_data(json=False)
        user_json['password'] = 'abcdefgh'
        user_json['retype_password'] = 'abcdefgh'
        with self.app.app_context(), self.assertRaises(RequestDataException) as error_context:
            schema.validate_password_strength(user_json)
        eq_(error_context.exception.errors, Failures.passwords_too_week)

    @patch('passport.api.users.schema.db')
    @patch('passport.api.users.schema.User')
    def test_user_load_email_registered(self, mock_user, mock_db):
        schema = UserSchema()
        user_json = user_data(json=False)
        mock_user.query.filter.return_value.first.return_value = User(email=user_json['email'])
        mock_db.or_.return_value = 'test'
        with self.app.app_context(), self.assertRaises(AccountException) as error_context:
            response_object, errors = schema.load(user_json)
        eq_(error_context.exception.errors, Failures.email_already_registered)

    @patch('passport.api.users.schema.db')
    @patch('passport.api.users.schema.User')
    def test_user_load_username_registered(self, mock_user, mock_db):
        schema = UserSchema()
        user_json = user_data(json=False)
        mock_user.query.filter.return_value.first.return_value = User(username=user_json['username'])
        mock_db.or_.return_value = 'test'
        with self.app.app_context(), self.assertRaises(AccountException) as error_context:
            response_object, errors = schema.load(user_json)
        eq_(error_context.exception.errors, Failures.username_already_exists)

    @patch('passport.api.users.schema.db')
    @patch('passport.api.users.schema.User')
    def test_user_load_missing_fields(self, mock_user, mock_db):
        schema = UserSchema()
        user_json = user_data(json=False)

        required_fields = self.get_schema_required_fields(UserSchema)
        [user_json.pop(k) for k in required_fields]

        mock_user.query.filter.return_value.first.return_value = None
        mock_db.or_.return_value = 'test'

        with self.assertRaises(RequestDataException) as error_context:
            response_object, error = schema.load(user_json)

        eq_(
            set(error_context.exception.errors['details'].keys()) -
            set(required_fields),
            set([]))
        error_context.exception.errors['details'] = None
        eq_(error_context.exception.errors, CommonFailures.information_missing)

    def get_schema_required_fields(self, schema):
        return [k for k, v in schema._declared_fields.iteritems()
                if v.required and not v.dump_only]