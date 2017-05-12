# coding: utf-8
from flask import jsonify, render_template, request, session, redirect
from flask_restful import Resource
from flask_security import login_required
from flask_oauthlib.utils import extract_params, create_response
import requests

from ..common import api

from ...extensions import oauth
from ...models import Client


@api.resource('/authorize')
class AuthorizeResource(Resource):

    def authorize(self, *args, **kwargs):
        """When consumer confirm the authorization."""

        server = oauth.server
        scope = request.values.get('scope') or ''
        scopes = scope.split()
        credentials = dict(
            client_id=request.values.get('client_id'),
            redirect_uri=request.values.get('redirect_uri', None),
            response_type=request.values.get('response_type', None),
            state=request.values.get('state', None)
        )
        redirect_uri = credentials.get('redirect_uri')
        print('Found redirect_uri %s.', redirect_uri)

        uri, http_method, body, headers = extract_params()
        request.client_id = credentials['client_id']
        ret = server.create_authorization_response(
            uri, http_method, body, headers, scopes, credentials)
        print('Authorization successful.')
        
        return ret
        #return True

    @login_required
    def get(self, *args, **kwargs):
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = session['user_id']
        
        #requests.post('')
        ret = self.authorize(None, kwargs)
        return create_response(*ret)
        #return render_template('authorize.html', **kwargs)
