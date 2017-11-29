from unittest import TestCase

from nose.tools import assert_is_not_none, eq_
from mock import patch, mock_open

from passport import create_app
from passport.api.exceptions import ApiException, RequestDataException
from passport.api.common.failures import Failures as CommonFailures
from passport.api.clients import service
from passport.models import Client

from ...mocks.common import client_data


class ServiceTests(TestCase):


    def setUp(self):
        self.app = create_app(settings_override={
            'SQLALCHEMY_DATABASE_URI': "sqlite://"
        })
        self.app.config['TESTING'] = True

    @patch('passport.api.clients.service.Client')
    def test_list_clients_id_filter(self, mock_client):
        client_json = client_data()
        
        client = Client(**client_json)
        mock_client.query.filter_by.return_value.all.return_value = [client]
        with self.app.test_request_context('/?name=Peter'):
            result_client = service.list_clients(client_id=1)
            eq_(result_client[0], client)

    @patch('passport.api.clients.service.Client')
    def test_list_clients(self, mock_client):
        client_json = client_data()
        
        client = Client(**client_json)
        mock_client.query.all.return_value = [client]
        with self.app.test_request_context('/?name=Peter'):
            result_client = service.list_clients()
            eq_(result_client[0], client)

    @patch('passport.api.clients.service.db')
    def test_create_client_credentials(self, mock_db):
        client_json = client_data()
        
        client = Client(**client_json)
        mock_db.session.add.return_value = "test"
        mock_db.session.commit.return_value = "test"
        with self.app.test_request_context('/?name=Peter'):
            result_client = service.create_client_credentials(client)
            eq_(result_client._default_scopes, 'email')
            assert_is_not_none(result_client.client_id)
            assert_is_not_none(result_client.client_secret)

    def test_create_credentials_response(self):
        client_json = client_data()
        client = Client(**client_json)
        client.client_id = 'client_id'
        client.client_secret = 'client_secret'

        result_json = service.create_credentials_response(client)    
        eq_(result_json['client_id'], 'client_id')
        eq_(result_json['client_secret'], 'client_secret')

    @patch('passport.api.clients.service.create_client_credentials')
    @patch('passport.api.clients.service.db')
    @patch('passport.api.clients.service.Client')
    def test_reset_credentials(self, mock_client, mock_db, mock_create_credentials):
        client_json = client_data()
        client = Client(**client_json)
        client.client_id = 'client_id'
        client.client_secret = 'client_secret'

        mock_db.session.commit.return_value = 'test'
        mock_client.query.filter_by.return_value.first.return_value = client
        mock_create_credentials.return_value = client
        result_json = service.reset_credentials(client_json['name'])
        eq_(result_json['client_id'], 'client_id')
        eq_(result_json['client_secret'], 'client_secret')


