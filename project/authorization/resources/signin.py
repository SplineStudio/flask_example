from . import (
    create_access_token,
    create_refresh_token,
    jsonify,
    reqparse,
    Resource,
    User
)
from project.errors.custom_exceptions import UserNotExist, WrongPassword

parser = reqparse.RequestParser()
parser.add_argument('email', dest='email', required=True, location='json')
parser.add_argument('password', dest='password', required=True, location='json')


class SignIn(Resource):

    def post(self):

        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()

        if not user:
            raise UserNotExist

        if not user.check_password(args['password']):
            raise WrongPassword

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify(dict(
            success=True,
            message='Ok',
            access_token=access_token,
            refresh_token=refresh_token
        ))



