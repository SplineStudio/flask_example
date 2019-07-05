from flask import jsonify
from flask_jwt_extended import jwt_required

from . import Resource


class ProtectedPage(Resource):

    @jwt_required
    def get(self):
        response = dict(code=1, message='This is secret page')

        return jsonify(response)
