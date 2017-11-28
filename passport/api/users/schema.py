import re

from flask_security.utils import encrypt_password
from marshmallow import post_load, validates_schema

from ..common.failures import Failures as CommonFailures
from ..exceptions import AccountException, RequestDataException
from ..extensions import schemas
from ..persons.schema import PersonSchema
from ..roles.schema import RoleSchema

from ...extensions import db
from ...models import Role, User

from .failures import Failures


class UserSchema(schemas.Schema):
    id = schemas.Integer()
    username = schemas.String(required=True)
    email = schemas.String(required=True)
    password = schemas.String(required=True, load_only=True)
    retype_password = schemas.String(required=True, load_only=True)
    active = schemas.Boolean()
    confirmed_at = schemas.DateTime(required=True, dump_only=True)
    roles = schemas.Nested(RoleSchema, many=True, load_only=True)
    person = schemas.Nested(PersonSchema)

    def handle_error(self, exc, data):
        response = CommonFailures.information_missing
        response['details'] = exc.message
        raise RequestDataException(response)

    @validates_schema(skip_on_field_errors=True)
    def validate_passwords(self, data):
        if not data['password']:
            raise RequestDataException(Failures.empty_password)
        elif data['password'] != data['retype_password']:
            raise RequestDataException(Failures.passwords_doesnt_match)

    @validates_schema(skip_on_field_errors=True)
    def validate_password_strength(self, data):
        pattern = re.compile(
            r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
        found = pattern.match(data['password'])
        if found is None:
            raise RequestDataException(Failures.passwords_too_week)

    @validates_schema(skip_on_field_errors=True)
    def validate_username_email(self, data):
        user = User.query.filter(db.or_(
            User.email == data['email'],
            User.username == data['username']
        )).first()

        if user is not None:
            failure = None
            if user.email == data['email']:
                failure = Failures.email_already_registered
            else:
                failure = Failures.username_already_exists

            raise AccountException(failure)

    @post_load
    def make_user(self, data):
        data.pop('retype_password')
        data['password'] = encrypt_password(data['password'])
        return User(**(data or {}))
