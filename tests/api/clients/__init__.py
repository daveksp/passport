import json
from unittest import TestCase

from nose.tools import assert_is_not_none, eq_

from ..base import AppCreator
from ...mocks.common import client_data

from passport.models import Client


class ClientTests(TestCase):
    __metaclass__ = AppCreator

    def test_put(self):
        with self.app.app_context():
    	    client = Client.query.filter_by(name='Test Client').first()
    	client_json = client_data()
    	client_json['name'] = 'Updated Client'
    	client_json['id'] = client.id
        response = self.client.put(
        	'/passport/api/v1/auth/clients/{}'.format(client.id),
        	data=json.dumps(client_json),
            headers=self.json_header)
        response_data = json.loads(response.data)
        eq_(response_data['client_id'], 'abcd')
        eq_(response_data['client_secret'], 'abcd')

    def test_post(self):
    	client_json = client_data()
    	client_json['name'] = 'New Client'
        response = self.client.post(
        	'/passport/api/v1/auth/clients',
        	data=json.dumps(client_json),
            headers=self.json_header)

        response_data = json.loads(response.data)
        assert_is_not_none(response_data['client_id'])
        assert_is_not_none(response_data['client_secret'])
