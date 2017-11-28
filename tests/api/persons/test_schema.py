from unittest import TestCase

from nose.tools import eq_
from mock import patch, mock_open

from passport import create_app
from passport.api.exceptions import ApiException, RequestDataException
from passport.api.common.failures import Failures as CommonFailures
from passport.api.persons.schema import PersonSchema
from passport.models import Person

from ...mocks.common import person_data


class SchemaTests(TestCase):


    def setUp(self):
        self.app = create_app(settings_override={
            'SQLALCHEMY_DATABASE_URI': "sqlite://"
        })
        self.app.config['TESTING'] = True

    def test_person_load(self):
        schema = PersonSchema()
        person_json = person_data(json=False)
        with self.app.app_context():
            response_object, errors = schema.load(person_json)

    def test_person_load_missing_fields(self):
        schema = PersonSchema()
        person_json = person_data(json=False)

        required_fields = self.get_schema_required_fields(PersonSchema)
        [person_json.pop(k) for k in required_fields]

        with self.assertRaises(RequestDataException) as error_context:
            response_object, error = schema.load(person_json)

        eq_(
            set(error_context.exception.errors['details'].keys()) -
            set(required_fields),
            set([]))
        error_context.exception.errors['details'] = None
        eq_(error_context.exception.errors, CommonFailures.information_missing)

    def get_schema_required_fields(self, schema):
        return [k for k, v in schema._declared_fields.iteritems()
                if v.required and not v.dump_only]