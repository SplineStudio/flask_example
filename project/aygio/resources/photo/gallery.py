from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import fields, marshal_with, Resource

from project.authorization.models import User
from project.aygio.models.photo import Photo
from project.errors.custom_exceptions import UserNotExist

users_photo_fields = {
        'id': fields.Integer,
        'file_name': fields.String
    }

props_photo_fields = {
        'id': fields.Integer,
        'file_name': fields.String,
        'property_id': fields.Integer
    }


class Gallery(Resource):

    @staticmethod
    @marshal_with(users_photo_fields)
    def users_photo_by_json(photo):
        return photo

    @staticmethod
    @marshal_with(props_photo_fields)
    def props_photo_by_json(photo):
        return photo

    @jwt_required
    def get(self):

        user = User.query.filter_by(id=get_jwt_identity()).first()
        if not user:
            raise UserNotExist

        arr_photo = Photo.query.filter_by(user_id=user.id).all()

        arr_users_photo = []
        arr_props_photo = []

        for photo in arr_photo:
            if photo.property_id:
                arr_props_photo.append(Gallery.props_photo_by_json(photo))
            else:
                arr_users_photo.append(Gallery.users_photo_by_json(photo))

        return jsonify(dict(
            success=True,
            users_photos=arr_users_photo,
            props_photos=arr_props_photo)
        )
