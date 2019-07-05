from flask import Blueprint
from flask_restful import Api

from .resources.signin import SignIn
from .resources.signup import SignUp
from .resources.refresh_token import RefreshToken
from .resources.request_recovery import RequestRecovery
from .resources.recovery_password import RecoveryPassword

bp = Blueprint('authorization', __name__)
api = Api(bp)

api.add_resource(SignIn, '/api/signin')
api.add_resource(SignUp, '/api/signup')
api.add_resource(RefreshToken, '/api/refreshtoken')
api.add_resource(RequestRecovery, '/api/requestrecovery')
api.add_resource(RecoveryPassword, '/api/recoverypassword')
