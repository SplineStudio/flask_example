from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import fields, marshal_with, Resource
from project.authorization.models import User
from project.aygio.models.system import DataSystem, DirSystem
from project.errors.custom_exceptions import SysNotExist, UserNotExist


class GetUserSystems(Resource):

    system_fields = {
        'system_id': fields.String,
        'name': fields.String,
        'url_img': fields.String,
    }

    @staticmethod
    @marshal_with(system_fields)
    def sys_by_json(sys_info):
        return dict(
            system_id=sys_info.id,
            name=sys_info.name,
            url_img=sys_info.url_img
        )

    @jwt_required
    def get(self):

        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        if not user:
            raise UserNotExist

        user_systems = DataSystem.query.filter_by(user_id=user.id).all()

        json_syss = []
        for sys in user_systems:
            sys_info = DirSystem.query.filter_by(id=sys.system_id).first()

            if not sys_info:
                raise SysNotExist

            json_syss.append(GetUserSystems.sys_by_json(sys_info))

        return jsonify(
            success=True,
            systems=json_syss
        )


