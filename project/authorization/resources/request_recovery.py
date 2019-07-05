import random
import string

from datetime import datetime
from flask import current_app, render_template
from flask_mail import Message
from . import (
    db,
    jsonify,
    reqparse,
    Resource,
    User
)

from project.mail import mail
from project.errors.custom_exceptions import UserNotExist

parser = reqparse.RequestParser()
parser.add_argument('email', dest='email', required=True, location='json')


def generate_code(code_size):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(code_size))


class RequestRecovery(Resource):
    def post(self):

        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()

        if not user:
            raise UserNotExist

        code_length = current_app.config['RECOVERY_CODE_LENGHT']
        code = generate_code(code_size=code_length)
        while User.query.filter_by(code_recovery=code).first():
            code = generate_code(code_length)

        user.code_recovery = code
        user.date_code_recovery = datetime.now()

        db.session.add(user)
        db.session.commit()

        msg = Message('Password recovery',
                      sender='robot@aygio.com',
                      recipients=['kudinov.mykola@gmail.com', user.email])
        msg.body = render_template('recovery_mail.txt', name=user.last_name, code=user.code_recovery)
        msg.html = render_template('recovery_mail.html', name=user.last_name, code=user.code_recovery)

        try:
            mail.send(msg)
            return jsonify(dict(success=True, message='Ok'))
        except:
            return jsonify(dict(success=False, message='Message not sending'))
