# coding: utf-8
from flask import Blueprint, make_response, render_template
from flask_restful import Resource
from flask_security import login_required

from ...clients.service import list_clients


admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='admin_templates')


@admin.route('/', methods=['GET'])
@login_required
def index():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template(
        'index.html'), headers)


@admin.route('/clients', methods=['GET'])
@login_required
def clients():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template(
        'clients.html', clients=list_clients(), operation_type='list'))
