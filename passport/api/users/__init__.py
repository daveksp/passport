# coding: utf-8
from flask import jsonify, make_response, request
from flask_restful import Resource

from schema import PersonSchema
from service import save_photo
from ..common import api
from ...extensions import db, oauth


@api.resource('/users')
class UsersResource(Resource):

    @oauth.require_oauth()
    def get():
        user = request.oauth.user
        return jsonify(username=user.username)

    def post(self):
        schema = PersonSchema()
        person, errors = schema.load(request.json or {})
        person.user.active = True

        user_photo = request.files.get('photo', None)
        if user_photo is not None:
            photo_url = save_photo(user_photo, person.user)

        db.session.add(person)
        db.session.commit()

        response, response_errors = schema.dump(person)
        return make_response(jsonify(response), 201)
