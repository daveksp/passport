from unittest import TestCase

from nose.tools import eq_
from mock import patch, mock_open

from passport.api.roles import service
from passport.models import Role
from passport import create_app

from ...mocks.common import role_data


class ServiceTests(TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

    @patch('passport.api.roles.service.Role')
    def test_list_roles_id_filter(self, mock_role):
        role_json = role_data()
        
        role = Role(**role_json)
        mock_role.query.filter_by.return_value.all.return_value = [role]
        with self.app.test_request_context('/?name=Peter'):
            result_role = service.list_roles(role_id=1)
            eq_(result_role[0], role)

    @patch('passport.api.roles.service.Role')
    def test_list_roles(self, mock_role):
        role_json = role_data()
        
        role = Role(**role_json)
        mock_role.query.all.return_value = [role]
        with self.app.test_request_context('/?name=Peter'):
            result_role = service.list_roles()
            eq_(result_role[0], role)
