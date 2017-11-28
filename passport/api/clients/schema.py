from marshmallow import post_load, validates_schema

from ..common.failures import Failures as CommonFailures
from ..exceptions import RequestDataException
from ..extensions import schemas

from ...extensions import db
from ...models import Client

from .failures import Failures


class ClientSchema(schemas.Schema):
    id = schemas.Integer(required=True)
    name = schemas.String(required=True)
    description = schemas.String(required=True)
    redirect_uris = schemas.String(required=True)

    def handle_error(self, exc, data):
        response = CommonFailures.information_missing
        response['details'] = exc.message
        raise RequestDataException(response)

    @validates_schema(skip_on_field_errors=True)
    def validate_name(self, data):
        if 'id' not in data or not data['id']:
            client = Client.query.filter(Client.name == data['name']).first()

            if client is not None:
                failure = Failures.client_name_already_exists
                failure['message'] = "client name already registered" 
                failure['details'] = "the name of your choice is already in usage"
                raise RequestDataException(failure)

    @post_load
    def make_user(self, data):
        return Client(**(data or {}))
