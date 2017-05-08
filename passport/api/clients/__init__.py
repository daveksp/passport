# coding: utf-8
from flask import jsonify, render_template, request, session
from flask_restful import Resource
from flask_security import login_required

from service import (create_client, create_credentials_response,
                     load_client, reset_credentials)
from ..common import api

from ...models import User


@api.resource('/clients')
class ClientsResource(Resource):

    @login_required
    def get(self):
        return render_template(
            'clients.html', users=User.query.filter_by(id=session['user_id']))

    def post(self):
        name = request.json['name']
        redirect_uri = request.json['redirect_uri']
        client = create_client(name, redirect_uri)
        return jsonify(create_credentials_response(client))

    def put(self):
        name = request.json['name']
        return jsonify(reset_credentials(name))
