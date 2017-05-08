# coding: utf-8
from flask_restful import Resource

from service import load_token, save_token
from ..common import api
from ...extensions import oauth


@api.resource('/token')
class TokensResource(Resource):

    @oauth.token_handler
    def get(self):
        return None

    @oauth.token_handler
    def post(self):
        return None
