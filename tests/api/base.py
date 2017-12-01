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


test_objects = {}

def create_test_objects():
    if not test_objects:
        json_header = {'Content-Type': 'application/json'}
        app = create_app(settings_override={
            'SQLALCHEMY_DATABASE_URI': "sqlite://"
        })
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True

        with app.app_context():
            recreate_db(db)

        client = Client(**client_data())
        client._default_scopes = 'email'
        client.client_id = 'abcd'
        client.client_secret = 'abcd'
        with app.app_context():
            user = User.query.get(1)
            client.user = user
            db.session.add(client)
            db.session.commit()
        app.login_manager.init_app(app)
        app_client = app.test_client()
        rv = app_client.post('/auth/token', data={
            'grant_type': 'client_credentials',
            'client_id': 'abcd',
            'client_secret': 'abcd',
        })
        response = json.loads(rv.data)
        header = {'Authorization': 'Bearer {0}'.format(response['access_token'])}
        json_header.update(header)
        test_objects['header'] = header
        test_objects['json_header'] = json_header
        test_objects['app'] = app
        test_objects['client'] = app_client
    return test_objects


class AppCreator(type):

    
    def __new__(cls, name, bases, namespace, **kwds):
        result = type.__new__(cls, name, bases, dict(namespace))
        test_objects = create_test_objects()
        result.app = test_objects['app']
        result.json_header = test_objects['json_header']
        result.header = test_objects['header']
        result.client = test_objects['client']
        return result
