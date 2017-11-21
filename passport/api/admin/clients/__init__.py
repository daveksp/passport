# coding: utf-8
from flask import Blueprint, make_response, render_template
from flask_restful import Resource
from flask_security import login_required

from ...api.clients.service import list_clients

"""
api = Blueprint('admin', __name__, url_prefix='/admin')


@login_required
@api.route('/', methods=['GET'])
def index():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template(
        'index.html'), headers)

@login_required
@api.route('/clients', methods=['GET'])
def index():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template(
        'clients.html', clients=list_clients(), operation_type=list), headers)
"""