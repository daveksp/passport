# coding: utf-8
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from .service import generate_jwt
from ...extensions import oauth

blueprint = Blueprint(
    'api', __name__, url_prefix='/api')

api = Api(blueprint)


@api.resource('/me')
class PersonResource(Resource):

    @oauth.require_oauth()
    def get(self):
        user = request.oauth.user
        return jsonify({'jwt': generate_jwt(user)})
