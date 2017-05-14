# coding: utf-8
from flask import session
from flask_restful import Resource
from flask_security import login_required
from flask_oauthlib.utils import create_response

from ...extensions import oauth
from ...models import Client

from ..common import api

from .service import authorize


@api.resource('/authorize')
class AuthorizeResource(Resource):

    @login_required
    @oauth.authorize_handler
    def get(self, *args, **kwargs):
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = session['user_id']

        ret = authorize(None, kwargs)
        return create_response(*ret)
