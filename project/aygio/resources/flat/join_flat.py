from flask import request
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, Resource

from project.database import db
from project.aygio.models.flat import Flat
from project.aygio.models.property import Property
from project.errors.custom_exceptions import ConnectionToForeignData, PropNotExist, UnavailableProp

def array_type(value, name):
    full_json_data = request.get_json()
    my_list = full_json_data[name]
    if(not isinstance(my_list, (list))):
        raise ValueError("The parameter " + name + " is not a valid array")
    return my_list


parser = reqparse.RequestParser()
parser.add_argument('combine_name', required=True, location='json')
parser.add_argument('id_property_list', required=True, type=array_type, location='json')


class JoinFlat(Resource):

    @jwt_required
    def post(self):
        args = parser.parse_args()
        list_id = args['id_property_list']

        if len(list_id) == 0:
            raise PropNotExist

        curr_user_id = get_jwt_identity()
        list_properties = []

        for prop_id in list_id:
            prop = Property.query.filter_by(id=prop_id).first()

            if prop.flat_id:
                raise UnavailableProp
            if prop.local_user_id != curr_user_id:
                raise ConnectionToForeignData

            list_properties.append(prop)

        if len(list_properties) != len(list_id):
            raise PropNotExist

        flat = Flat(name=args['combine_name'], user_id=curr_user_id)

        db.session.add(flat)
        db.session.commit()
        db.session.refresh(flat)

        for item in list_properties:
            item.flat_id = flat.id
            db.session.add(item)

        db.session.commit()
        db.session.close()

        return jsonify(dict(
            success=True
        ))



