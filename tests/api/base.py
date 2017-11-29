import datetime
import json
import os

from flask_testing import TestCase

from passport import create_app
from passport.extensions import db
from passport.tools.database import recreate_db

from passport.models import Client, Token, User

from ..mocks.common import client_data, user_data


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


class AppWrapper(object):

    def __init__(self, app, data, access_token):
        self.app = app
        self.data = data
        self.access_token = access_token

    def __call__(self, environ, start_response):
        environ['HTTP_AUTHORIZATION'] = self.access_token

        return self.app(environ, start_response)


class IntegrationTestCase(TestCase):

    header = {'Content-Type': 'application/json'}

    def create_app(self):
        self.app = create_app(settings_override={
            'SQLALCHEMY_DATABASE_URI': "sqlite://"
        })
        self.app.config['TESTING'] = True
        self.app.config['LOGIN_DISABLED'] = False

        with self.app.app_context():
            recreate_db(db)

        self.create_oauth_credentials()
        return self.app

    def create_oauth_credentials(self):
    	client = Client(**client_data())
        client._default_scopes = 'email'
        client.client_id = 'abcd'
        client.client_secret = 'abcd'
        with self.app.app_context():
            user = User.query.get(1)
            client.user = user
            db.session.add(client)
            db.session.commit()

    def create_oauth_header(self):
        rv = self.client.post('/auth/token', data={
            'grant_type': 'client_credentials',
            'client_id': 'abcd',
            'client_secret': 'abcd',
        })
        response = json.loads(rv.data)
        header['Authorization'] = 'Bearer {0}'.format(response['access_token'])
