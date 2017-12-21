# coding: utf-8
from flask import Blueprint, make_response, render_template, request
from flask_restful import Resource
from flask_security import login_required

from ..clients.service import list_clients
from ..roles.service import list_roles
from ...models import Client, Role


admin = Blueprint('admin', __name__, url_prefix='/passport/admin')


@admin.route('/', methods=['GET'])
@login_required
def index():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template(
        'index.html'), headers)


@admin.route('/clients/<client_id>', methods=['GET'])
@admin.route('/clients/new', methods=['GET'])
@admin.route('/clients', methods=['GET'])
@login_required
def clients(client_id=None):
    headers = {'Content-Type': 'text/html'}
    if request.path[-4:] == '/new':
        clients = [Client()]
        operation_type = 'new'
    else:
        clients = list_clients(client_id)
        operation_type = 'list' if not client_id else 'edit'

    return make_response(render_template(
        'clients.html', clients=clients, operation_type=operation_type))


@admin.route('/roles/<role_id>', methods=['GET'])
@admin.route('/roles/new', methods=['GET'])
@admin.route('/roles', methods=['GET'])
@login_required
def roles(role_id=None, operation_type=None):
    headers = {'Content-Type': 'text/html'}
    if request.path[-4:] == '/new':
        roles = [Role()]
        operation_type = 'new'
    if not operation_type:
        roles = list_roles(role_id)
        operation_type = 'list' if not role_id else 'edit'

    return make_response(render_template(
        'roles.html', roles=roles, operation_type=operation_type))
