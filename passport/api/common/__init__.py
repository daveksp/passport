# coding: utf-8
from flask import Blueprint
from flask_restful import Api


blueprint = Blueprint(
    'auth', __name__, url_prefix='/passport/api/v1/auth',
    template_folder='templates', static_folder="static")

api = Api(blueprint)
