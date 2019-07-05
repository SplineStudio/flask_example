from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, Resource

from project.authorization.models import User
from project.aygio.api_manager.getter_api import get_api_manager
from project.aygio.models.system import DataSystem
from project.aygio.services import refresh_by_user_id
from project.database import db
from project.errors.custom_exceptions import ReconnectSystem, UserNotExist


parser = reqparse.RequestParser()
parser.add_argument('system_id', type=int, dest='system_id', required=True, location='json')
parser.add_argument('oauth_token', dest='oauth_token', required=True, location='json')


class AddSystem(Resource):

    @jwt_required
    def post(self):

        user_id = get_jwt_identity()
        body = parser.parse_args()

        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserNotExist

        arr_sys = DataSystem.query.filter_by(user_id=user.id).all()

        if len(arr_sys) != 0:
            for item in arr_sys:
                if item.system_id == body['system_id']:
                    raise ReconnectSystem

        manager = get_api_manager(body['system_id'])

        data_system = DataSystem(
            user_id=user_id,
            system_id=body['system_id'],
            token=body['oauth_token'],
            name_slug=manager.load_slug(body['oauth_token'])
        )

        db.session.add(data_system)
        db.session.commit()
        db.session.close()

        refresh_by_user_id(user_id)

        return jsonify(dict(
            success=True,
            message='Ok'
        ))
