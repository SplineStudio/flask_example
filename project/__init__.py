from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_uploads import configure_uploads, patch_request_class
from config import ServerConfig

from .database import db
from .mail import mail
from .upload_files import photos

api = Api()
bcrypt = Bcrypt()
jwt_manager = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(ServerConfig)

    api.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    configure_uploads(app, photos)
    patch_request_class(app)

    from project.authorization import bp as authorization_bp
    from project.aygio import bp as aygio_bp
    from project.errors import bp as error_bp

    app.register_blueprint(authorization_bp)
    app.register_blueprint(aygio_bp)
    app.register_blueprint(error_bp)

    return app
