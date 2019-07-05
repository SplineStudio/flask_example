from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, Resource

from project.database import db
from project.authorization.models import User
from project.aygio.models.flat import Flat
from project.errors.custom_exceptions import (
    ConnectionToForeignData,
    FlatNotExist,
    UserNotExist)

parser = reqparse.RequestParser()
parser.add_argument('flat_id', type=int, required=True, location='json')
parser.add_argument('name', required=True, location='json')


class ChangeFlatName(Resource):

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserNotExist

        args = parser.parse_args()

        flat = Flat.query.filter_by(id=args['flat_id']).first()
        if not flat:
            raise FlatNotExist

        if not flat.user_id == user_id:
            raise ConnectionToForeignData

        flat.name = args['name']

        db.session.add(flat)
        db.session.commit()
        db.session.close()

        return jsonify(dict(
            success=True,
            message='Ok'
        ))
