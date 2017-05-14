# coding: utf-8
from flask import Blueprint, render_template


blueprint = Blueprint(
    'oauth', __name__, url_prefix='/oauth', template_folder='templates')


@blueprint.route('/register', methods=['GET'])
def home():
    return render_template('user.html')


@blueprint.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@blueprint.route('/reset_password', methods=['GET'])
def reset_password_form():
    return render_template('reset_password.html')
