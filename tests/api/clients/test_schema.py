from unittest import TestCase

from nose.tools import eq_
from mock import patch, mock_open

from passport import create_app
from passport.api.exceptions import ApiException, RequestDataException
from passport.api.common.failures import Failures as CommonFailures
from passport.api.clients.schema import ClientSchema
from passport.models import Client

from ...mocks.common import client_data


class SchemaTests(TestCase):


    def setUp(self):
        self.app = create_app(settings_override={
            'SQLALCHEMY_DATABASE_URI': "sqlite://"
        })
        self.app.config['TESTING'] = True

    @patch('passport.api.clients.schema.Client')
    def test_client_load(self, mock_client):
        schema = ClientSchema()
        client_json = client_data(json=False)
        client = Client(**client_json)
        mock_client.return_value = client
        mock_client.query.filter.return_value.first.return_value = None
        with self.app.app_context():
            response_object, errors = schema.load(client_json, partial=('id',))
        eq_(errors, {})
        eq_(response_object, client)

    @patch('passport.api.clients.schema.Client')
    def test_client_load_name_registered(self, mock_client):
        schema = ClientSchema()
        client_json = client_data(json=False)
        mock_client.query.filter.return_value.first.return_value = Client(name=client_json['name'])
        with self.app.app_context(), self.assertRaises(RequestDataException) as error_context:
            response_object, errors = schema.load(client_json, partial=('id',))
        failure = CommonFailures.name_already_exists
        failure['message'] = "client name already registered" 
        failure['details'] = "the name of your choice is already in usage"

        eq_(error_context.exception.errors, failure)

    @patch('passport.api.clients.schema.Client')
    def test_client_load_updating(self, mock_client):
        schema = ClientSchema()
        client_json = client_data(json=False)
        client_json['id'] = 1
        client = Client(**client_json)
        mock_client.return_value = client
        mock_client.query.filter.return_value.first.return_value = Client(name=client_json['name'])
        with self.app.app_context():
            response_object, errors = schema.load(client_json)
        eq_(errors, {})
        eq_(response_object ,client)        

    def test_client_load_missing_fields(self):
        schema = ClientSchema()
        client_json = client_data(json=False)
        client_json['id'] = 1
        required_fields = self.get_schema_required_fields(ClientSchema)
        [client_json.pop(k) for k in required_fields]

        with self.assertRaises(RequestDataException) as error_context:
            response_object, error = schema.load(client_json)

        eq_(
            set(error_context.exception.errors['details'].keys()) -
            set(required_fields),
            set([]))
        error_context.exception.errors['details'] = None
        eq_(error_context.exception.errors, CommonFailures.information_missing)

    def get_schema_required_fields(self, schema):
        return [k for k, v in schema._declared_fields.iteritems()
                if v.required and not v.dump_only]