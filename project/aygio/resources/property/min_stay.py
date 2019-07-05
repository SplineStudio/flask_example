from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, Resource

from project.database import db
from project.authorization.models import User

from project.aygio.api_manager.getter_api import get_api_manager
from project.aygio.models.flat import Flat
from project.aygio.models.property import Property
from project.aygio.models.system import DataSystem

from project.errors.custom_exceptions import (
    ConnectionToForeignData,
    FlatNotExist,
    PropNotExist,
    SysNotExist,
    UserNotExist
)


KEY_MIN_STAY = "min_stay"

parser = reqparse.RequestParser()
parser.add_argument('flat_id', type=int, required=True, location='json')
parser.add_argument(KEY_MIN_STAY, type=int, required=True, location='json')


class ChangeMinStay(Resource):

    @staticmethod
    def validate_user(user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserNotExist
        return user

    @staticmethod
    def validate_flat(flat_id, user):
        flat = Flat.query.filter_by(id=flat_id).first()

        if not flat:
            raise FlatNotExist

        if flat.user_id != user.id:
            raise ConnectionToForeignData

        return flat

    @staticmethod
    def validate_props(flat, user):
        props = Property.query.filter_by(flat_id=flat.id).all()

        if len(props) == 0:
            raise PropNotExist

        for pr in props:
            if pr.local_user_id != user.id:
                raise ConnectionToForeignData

        return props

    @jwt_required
    def post(self):

        args = parser.parse_args()

        user = ChangeMinStay.validate_user(get_jwt_identity())
        flat = ChangeMinStay.validate_flat(args['flat_id'], user)
        properties = ChangeMinStay.validate_props(flat, user)

        for prop in properties:
            data_system = DataSystem.query.filter_by(system_id=prop.system_id).first()
            if not data_system:
                raise SysNotExist

            manager = get_api_manager(data_system.system_id)
            manager.update_prop(prop.inner_id, data_system.token, KEY_MIN_STAY, args[KEY_MIN_STAY])

            prop.min_stay = args[KEY_MIN_STAY]

            db.session.add(prop)
            db.session.commit()
            db.session.close()

        return jsonify(dict(
            success=True
        ))
