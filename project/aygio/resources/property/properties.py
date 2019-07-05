from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import fields, marshal_with, Resource

from project.authorization.models import User
from project.aygio.models.property import Property

from project.errors.custom_exceptions import PropNotExist, UserNotExist

property_fields = {
        'id': fields.Integer,
        'system_id': fields.Integer,
        'name': fields.String,
        'country': fields.String,
        'city': fields.String,
        'district': fields.String,
        'zip_code': fields.String,
        'price': fields.Integer,
        'currency': fields.String,
        'min_stay': fields.Integer,
        'size': fields.Integer,
        'photo_url': fields.String,
        'number_of_guests': fields.Integer
    }


class Properties(Resource):

    @staticmethod
    @marshal_with(property_fields)
    def prop_by_json(prop):
        return prop

    @jwt_required
    def get(self):

        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserNotExist

        props = Property.query.filter_by(local_user_id=user.id).all()
        if len(props) == 0:
            raise PropNotExist

        json_props = []
        for prop in props:
            json_props.append(Properties.prop_by_json(prop))

        return jsonify(dict(
            success=True,
            properties=json_props
        ))
