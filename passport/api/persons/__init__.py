# coding: utf-8
import json

from flask import Blueprint, jsonify, request, make_response
from flask_restful import Api, Resource
from jose.exceptions import JWSError

from ...extensions import sentinel, oauth, store


blueprint = Blueprint(
    'api', __name__, url_prefix='/api')

api = Api(blueprint)


@api.resource('/person')
class PersonResource(Resource):

    def post(self):
        pass