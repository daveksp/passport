# coding: utf-8
from flask import jsonify, make_response, request
from flask_restful import Resource

from service import save_photo

from ..common import api
from ..persons.service import person_schema_load, save_and_dump_person
from ...extensions import oauth, sentinel, store


routes = ['/me', '/users']

@api.resource(*routes)
class UsersResource(Resource):

    def post(self):
        person = person_schema_load(request.json)
        person.user.active = True
        user_photo = request.files.get('photo', None)
        if user_photo is not None:
            photo_url = save_photo(user_photo, person.user)

        response = save_and_dump_person(person)
        return make_response(jsonify(response), 201)

    @oauth.require_oauth()
    def get(self):
        token = None
        oauth_token = request.headers['Authorization'].split('Bearer ')[1]
        if oauth_token in store:
            oauth_data = json.loads(store.get(oauth_token))
            try:
                user_data = sentinel.verify_jwt(oauth_data['jwt'])
                if user_data:
                    token = oauth_data['jwt']
            except JWSError as exc:
                token = oauth_token['jwt'] = sentinel.authorize(generate_jwt(
                    request.oauth.user))
                store.put(oauth_token, json.dumps(user_data))
        return jsonify({'user':user_data, 'jwt': token})
