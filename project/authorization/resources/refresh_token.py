from . import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jsonify,
    Resource,
    User
)
from project.errors.custom_exceptions import UserNotExist


class RefreshToken(Resource):

    @jwt_refresh_token_required
    def get(self):

        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserNotExist

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify(dict(success=True, message='Ok', access_token=access_token, refresh_token=refresh_token))

