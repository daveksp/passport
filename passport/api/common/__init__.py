# coding: utf-8
from flask import Blueprint
from flask_restful import Api


blueprint = Blueprint(
    'oauth', __name__, url_prefix='/oauth', template_folder='templates')

api = Api(blueprint)
