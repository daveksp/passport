# coding: utf-8
from flask import jsonify, make_response, render_template, request, session
from flask_restful import Resource
from flask_security import login_required

from schema import ClientSchema
from service import (create_client_credentials, create_credentials_response,
                     list_clients, load_client, reset_credentials)
from ..common import api
from ...models import User
from ...extensions import db


client_schema = ClientSchema()

@api.resource('/clients/<client_id>', endpoint='update_client')
@api.resource('/clients')
class ClientsResource(Resource):

    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template(
            'clients.html', users=User.query.filter_by(
                id=session['user_id'])), headers)

    @login_required
    def post(self):
        client = client_schema.load(request.json or {},partial=('id',))[0]
        client = create_client_credentials(client)
        return jsonify(create_credentials_response(client))

    def put(self, client_id):
        client_update, request_errors = client_schema.load(request.json or {})
        client = list_clients(client_id)[0] #add handler case not found
        client.name = client_update.name
        client.description = client_update.description
        client._redirect_uris = client_update._redirect_uris
        db.session.commit()
        return create_credentials_response(client)
