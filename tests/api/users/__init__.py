import json
from nose.tools import assert_is_not_none, eq_

from ..base import IntegrationTestCase
from ...mocks.common import user_data

from passport.models import User


class UserTests(IntegrationTestCase):


    def setUp(self):
        self.create_app()

    def test_get(self):
        response = self.client.get(
        	'/auth/users')
        
        response_data = json.loads(response.data)
        assert_is_not_none(response_data['jwt'])
        assert_is_not_none(response_data['user']['person'])
        assert_is_not_none(response_data['user']['username'])

    def test_post(self):
    	user_json = user_data()
        del user_json['confirmed_at']
        del user_json['id']
        response = self.client.post(
        	'/auth/users',
        	data=json.dumps(user_json),
            headers=self.header)

        response_data = json.loads(response.data)
        assert_is_not_none(response_data['person'])
        eq_(response_data['active'], True)
        eq_(response_data['email'], user_json['email'])
        eq_(response_data['username'], user_json['username'])
        eq_(response_data['person']['first_name'], user_json['person']['first_name'])
        eq_(response_data['person']['last_name'], user_json['person']['last_name'])

