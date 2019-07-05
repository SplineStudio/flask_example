from flask import Blueprint, jsonify
from flask_restful import Api
from flask_uploads import UploadNotAllowed
from email_validator import EmailNotValidError
from project.errors.custom_exceptions import DefaultException

bp = Blueprint('errors', __name__)
api = Api(bp)


@bp.app_errorhandler(DefaultException)
def handle_error(error):
    return jsonify(dict(success=False, message=error.message)), error.status_code


@bp.app_errorhandler(EmailNotValidError)
def handle_error(error):
    return jsonify(dict(success=False, message='Not valid mail')), 400


@bp.app_errorhandler(UploadNotAllowed)
def handle_error(error):
    return jsonify(dict(success=False, message='Attempt load incorrect file')), 422

