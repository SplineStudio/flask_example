from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from project.authorization.models import User
from project.aygio.services import refresh_by_user_id
from project.errors.custom_exceptions import (
    FailurePropsSystem,
    FailureSysManager,
    OldData,
    OutSystemConnect,
    SysNotExist,
    UserNotExist
)


class Refresh(Resource):

    @jwt_required
    def post(self):

        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserNotExist

        refresh_by_user_id(user_id)

        return jsonify(dict(
            success=True
        ))
