# coding: utf-8
from flask import Blueprint, make_response, render_template
from flask_restful import Resource
from flask_security import login_required

from ..clients.service import list_clients


admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='admin_templates')


@admin.route('/', methods=['GET'])
@login_required
def index():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template(
        'index.html'), headers)


@admin.route('/clients/<client_id>', methods=['GET'])
@admin.route('/clients', methods=['GET'])
@login_required
def clients(client_id=None):
    headers = {'Content-Type': 'text/html'}
    clients = list_clients(client_id)
    operation_type = 'list' if not client_id else 'edit'

    return make_response(render_template(
        'clients.html', clients=clients, operation_type=operation_type))
