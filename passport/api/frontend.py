# coding: utf-8
from flask import (jsonify, Blueprint, render_template, request, session)
from flask_security import login_required


blueprint = Blueprint(
    'auth', __name__, url_prefix='/auth', template_folder='templates')


@blueprint.route('/register', methods=['GET'])
def home():
    return render_template('user.html')


@blueprint.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@blueprint.route('/reset_password', methods=['GET'])
def reset_password_form():
    return render_template('reset_password.html')
