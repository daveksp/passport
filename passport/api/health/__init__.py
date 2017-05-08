from flask import Blueprint, jsonify
from flask_restful import Api, Resource


# named Blueprint object, so as to be registered by the app factory
blueprint = Blueprint('health', __name__, url_prefix='/health')
api = Api(blueprint)


@api.resource('')
class SkuResource(Resource):

    def get(self):
        """ Retrieve the health of the endpoint """

        return jsonify({"health": "Healthy"})
