from unittest import TestCase

from nose.tools import eq_
from mock import patch, mock_open

from passport.api.users import service
from passport.models import User
from passport import create_app

from ...mocks.common import user_data


class ServiceTests(TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True

    @patch('passport.api.users.service.User')
    @patch('passport.api.users.service.session')
    def test_current_user(self, mock_session, mock_user):
        good_user_data = user_data()
        del good_user_data['retype_password']
        user = User(**good_user_data)
        session_data = {'user_id': 1}
        mock_session.__getitem__.side_effect = session_data.__getitem__
        mock_session.__iter__.side_effect = session_data.__iter__
        mock_session.__contains__ = lambda s, o: o == 'user_id'
        mock_user.query.get.return_value = user
        with self.app.test_request_context('/?name=Peter'):
            result_user = service.current_user()
            eq_(result_user, user)

    @patch('passport.api.users.service.sentinel')
    @patch('passport.api.users.service.User')
    @patch('passport.api.users.service.session')
    def test_generate_jwt(self, mock_session, mock_user, mock_sentinel):
        good_user_data = user_data()
        del good_user_data['retype_password']
        user = User(**good_user_data)
        mock_session = {'user_id': 1}
        mock_user.query.filter_by.return_value.first.return_value = user
        mock_sentinel.authorize.return_value = 'test_token'
        token = service.generate_jwt(user)
        eq_(token, 'test_token')
