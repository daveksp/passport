from marshmallow import post_load

from ..common.failures import Failures as CommonFailures
from ..exceptions import RequestDataException
from ..extensions import schemas

from ...models import Person


class PersonSchema(schemas.Schema):

    first_name = schemas.String(required=True)
    last_name = schemas.String(required=True)
    photo = schemas.String()
    team = schemas.String()

    def handle_error(self, exc, data):
        response = CommonFailures.information_missing
        response['details'] = exc.message
        raise RequestDataException(response)

    @post_load
    def make_person(self, data):
        return Person(**(data or {}))
