from datetime import datetime, timedelta
from flask import current_app
from . import (
    db,
    jsonify,
    reqparse,
    Resource,
    User
)
from project.errors.custom_exceptions import OutDate, WrongCodeRecovery, UserNotExist


parser = reqparse.RequestParser()
parser.add_argument('email', dest='email', required=True, location='json')
parser.add_argument('code', dest='code', required=True, location= 'json')
parser.add_argument('password', dest='password', required=True, location='json')


def validate_date(user, period):
    target_date = user.date_code_recovery + timedelta(days=period)
    return target_date > datetime.now().date()


class RecoveryPassword(Resource):

    def post(self):

        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()

        if user.code_recovery != args['code']:
            raise WrongCodeRecovery

        if not user:
            raise UserNotExist

        if not validate_date(user=user, period=current_app.config['PERIOD_RECOVERY_CODE']):
            raise OutDate

        if not user.check_password(args['password']):
            user.set_password(args['password'])

        user.code_recovery = None
        user.date_code_recovery = None
        db.session.add(user)
        db.session.commit()

        return jsonify(dict(success=True, message='Ok'))
