from flask import current_app, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, Resource
from werkzeug import FileStorage, secure_filename

from project.authorization.models import User
from project.database import db
from project.aygio.models.photo import Photo
from project.errors.custom_exceptions import PhotoNotExist, UserNotExist
from project.upload_files import photos


parser = reqparse.RequestParser()
parser.add_argument('photo', type=FileStorage, required=True, location='files')


class UploadPhoto(Resource):

    @jwt_required
    def post(self):

        user_id = get_jwt_identity()
        if not User.query.filter_by(id=user_id).first():
            raise UserNotExist

        args = parser.parse_args()
        file = args['photo']
        filename = secure_filename(file.filename)

        if filename == '' or not file:
            raise PhotoNotExist

        photos.save(file)
        full_name = current_app.config['HOST'] + current_app.config['UPLOADED_PHOTOS_DEST'] + '/' + filename

        photo = Photo(file_name=full_name, user_id=get_jwt_identity())
        db.session.add(photo)
        db.session.commit()

        return jsonify(dict(
            success=True,
            message='Ok'
        ))
