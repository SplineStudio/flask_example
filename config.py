from datetime import timedelta


DEV_POSTGRES = {
    'user': 'aygio_prod',
    'pw': 'CRneQDD2bK',
    'db': 'aygio_prod',
    'host': 'aygio.com',
    'port': '5432',
}

SERVER_POSTGRES = {
    'user': 'aygio_prod',
    'pw': 'CRneQDD2bK',
    'db': 'aygio_prod',
    'host': 'aygio.com',
    'port': '5432',
}


class BaseConfig:
    BUNDLE_ERRORS = True
    CSRF_ENABLED = True
    PROPAGATE_EXCEPTIONS = True
    HOST = "http://127.0.0.1:5000/"

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    JWT_TOKEN_LOCATION = 'headers'
    JWT_SECRET_KEY = 'salkfjdsaljgkldsmv,.cmxsdfalk;s;l;klkokiopopol;la;lodkfdasoferos;'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = ''
    JWT_ERROR_MESSAGE_KEY = 'Invalid token'
    RECOVERY_CODE_LENGHT = 6
    PERIOD_RECOVERY_CODE = 14  # days

    UPLOADED_PHOTOS_DEST = 'static/img'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    MAIL_SERVER = 'vps.aygio.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'robot@aygio.com'
    MAIL_PASSWORD = 'vrccVN2_E7'


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % DEV_POSTGRES


class ServerConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % SERVER_POSTGRES










