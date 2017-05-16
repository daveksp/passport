# coding: utf-8
from flask import jsonify, make_response, request
from flask_restful import Resource

from service import save_photo

from ..common import api
from ..persons.service import person_schema_load, save_and_dump_person


@api.resource('/users')
class UsersResource(Resource):

    def post(self):
        person = person_schema_load(request.json)
        person.user.active = True

        user_photo = request.files.get('photo', None)
        if user_photo is not None:
            photo_url = save_photo(user_photo, person.user)

        response = save_and_dump_person(person)
        return make_response(jsonify(response), 201)
