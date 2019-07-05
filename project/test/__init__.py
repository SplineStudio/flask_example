from flask import Blueprint
from flask_restful import Api

from .resources.index import Index
from .resources.protected_page import ProtectedPage

bp = Blueprint('test', __name__)
api = Api(bp)

api.add_resource(Index, '/api/index')
api.add_resource(ProtectedPage, '/api/protected')

