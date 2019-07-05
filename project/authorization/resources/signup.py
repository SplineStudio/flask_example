from email_validator import validate_email
from . import (
    db,
    jsonify,
    create_access_token,
    create_refresh_token,
    reqparse,
    Resource,
    User
)
from project.errors.custom_exceptions import UserExist

parser = reqparse.RequestParser()
parser.add_argument('first_name', dest='first_name', required = True, location= 'json')
parser.add_argument('last_name', dest='last_name', required = True, location= 'json')
parser.add_argument('email', dest='email', required = True, location= 'json')
parser.add_argument('password', dest='password', required = True, location= 'json')


class SignUp(Resource):

    def post(self):
        args = parser.parse_args()
        validate_email(args['email'])

        if User.query.filter_by(email=args['email']).first():
            raise UserExist

        user = User(first_name=args['first_name'], last_name=args['last_name'], email=args['email'])
        user.set_password(args['password'])

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify(dict(
            message='Ok',
            access_token=access_token,
            refresh_token=refresh_token))



