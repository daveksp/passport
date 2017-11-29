import json
from nose.tools import assert_is_not_none, eq_

from ..base import IntegrationTestCase
from ...mocks.common import client_data

from passport.models import Client


class ClientTests(IntegrationTestCase):

    def setUp(self):
        self.create_app()
        self.create_oauth_header()

    def test_put(self):
    	client = Client.query.filter_by(name='Test Client').first()
    	client_json = client_data()
    	client_json['name'] = 'Updated Client'
    	client_json['id'] = client.id
        response = self.client.put(
        	'/auth/clients/{}'.format(client.id),
        	data=json.dumps(client_json),
            headers=self.header)
        response_data = json.loads(response.data)
        eq_(response_data['client_id'], 'abcd')
        eq_(response_data['client_secret'], 'abcd')

    def est_post(self):
    	client_json = client_data()
    	client_json['name'] = 'New Client'
        response = self.client.post(
        	'/auth/clients',
        	data=json.dumps(client_json),
            headers=self.header)

        import pdb; pdb.set_trace()
        response_data = json.loads(response.data)
        assert_is_not_none(response_data['client_id'])
        assert_is_not_none(response_data['client_secret'])
