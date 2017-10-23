# coding: utf-8
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from jose.exceptions import JWSError

from .service import generate_jwt
from ...extensions import jwt, oauth, store


blueprint = Blueprint(
    'api', __name__, url_prefix='/api')

api = Api(blueprint)


@api.resource('/me')
class PersonResource(Resource):

    @oauth.require_oauth()
    def get(self):
        token = None
        oauth_token = request.headers['Authorization'].split('Bearer ')[1]
        if oauth_token in store:
            try:
                token = jwt.validate_token(store.get(oauth_token))
            except JWSError as exc:
                user = request.oauth.user
                token = jwt.authorize(generate_jwt(user))
                store.put(oauth_token, token)
        
        response = jsonify({'jwt': token})
        response.headers['Authorization'] = token
        return response
