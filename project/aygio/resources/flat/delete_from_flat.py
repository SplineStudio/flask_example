from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, Resource

from project.database import db
from project.authorization.models import User
from project.aygio.models.flat import Flat
from project.aygio.models.property import Property
from project.errors.custom_exceptions import (
    ConnectionToForeignData,
    ConnectionOccupiedProperty,
    EmptyListOnRequest,
    FlatNotExist,
    FlatWithoutProperty,
    ForeignProperty,
    PropNotExist,
    SysNotExist,
    UserNotExist
)


def array_type(value, name):
    full_json_data = request.get_json()
    my_list = full_json_data[name]
    if(not isinstance(my_list, (list))):
        raise ValueError("The parameter " + name + " is not a valid array")
    return my_list


parser = reqparse.RequestParser()
parser.add_argument('flat_id', required=True, location='json')
parser.add_argument('id_property_list', required=True, type=array_type, location='json')


class DeleteFromFlat(Resource):

    @staticmethod
    def validate_flat(flat, curr_user_id):
        if not flat:
            raise FlatNotExist
        if not curr_user_id == flat.user_id:
            raise ConnectionToForeignData

    @staticmethod
    def validate_property(prop, curr_user_id, flat_id):
        if not prop:
            raise PropNotExist

        if prop.local_user_id != curr_user_id:
            raise ConnectionToForeignData

        if not prop.flat_id:
            raise FlatWithoutProperty

        if prop.flat_id == flat_id:
            raise ForeignProperty

    @jwt_required
    def post(self):

        args = parser.parse_args()

        list_id = args['id_property_list']
        if len(list_id) == 0:
            raise EmptyListOnRequest

        curr_user_id = get_jwt_identity()
        if not User.query.filter_by(id=curr_user_id).first():
            raise UserNotExist

        flat = Flat.query.filter_by(id=args['flat_id']).first()

        DeleteFromFlat.validate_flat(flat, curr_user_id)

        list_properties = []
        for prop_id in list_id:
            prop = Property.query.filter_by(id=prop_id).first()
            DeleteFromFlat.validate_property(prop, curr_user_id , flat)
            list_properties.append(prop)

        if len(list_properties) != len(list_id):
            raise PropNotExist

        for item in list_properties:
            item.flat_id = None
            db.session.add(item)

        if not Property.query.filter_by(flat_id=flat.id).first():
            db.session.delete(flat)

        db.session.commit()
        db.session.close()

        return jsonify(dict(
            success=True
        ))
