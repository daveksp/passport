import json
from unittest import TestCase

from nose.tools import assert_is_not_none, eq_

from ..base import AppCreator
from ...mocks.common import role_data

from passport.models import Role
from passport.extensions import db

class RoleTests(TestCase):
    __metaclass__ = AppCreator

    def test_put(self):
        role_json = role_data()
        with self.app.app_context():
            role = Role(**role_json)
            db.session.add(role)
            db.session.commit()
            
    	    role_json['name'] = 'Updated Role'
    	    role_json['id'] = role.id
            response = self.client.put(
        	    '/auth/roles/{}'.format(role.id),
        	    data=json.dumps(role_json),
                headers=self.json_header)
            response_data = json.loads(response.data)
            eq_(response_data['description'], role_json['description'])
            eq_(response_data['name'], role_json['name'])
            assert_is_not_none(response_data['id'])

    def test_post(self):
    	role_json = role_data()
    	role_json['name'] = 'New Role'
        response = self.client.post(
        	'/auth/roles',
        	data=json.dumps(role_json),
            headers=self.json_header)

        response_data = json.loads(response.data)
        eq_(response_data['description'], role_json['description'])
        eq_(response_data['name'], role_json['name'])
        assert_is_not_none(response_data['id'])
