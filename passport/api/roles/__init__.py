# coding: utf-8
from flask import jsonify, make_response, render_template, request
from flask_restful import Resource
from flask_security import login_required

from schema import RoleSchema
from service import list_roles
from ..common import api
from ...extensions import db


role_schema = RoleSchema()

@api.resource('/roles/<role_id>', endpoint='update_role')
@api.resource('/roles')
class RoleResource(Resource):

    @login_required
    def post(self):
        role = role_schema.load(request.json or {}, partial=('id',))[0]
        db.session.add(role)
        db.session.commit()
        response, errors = role_schema.dump(role)
        return jsonify(response)

    def put(self, role_id):
        role_update, request_errors = role_schema.load(request.json or {})
        role = list_roles(role_id)[0] #add handler case not found
        role.name = role_update.name
        role.description = role_update.description
        db.session.commit()
        response, errors = role_schema.dump(role)
        return jsonify(response)
