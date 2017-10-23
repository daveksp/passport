import logging

from ..api.utilities import project_path


class Common(object):

    SECRET_KEY = 'SECRET'
    DEBUG = True
    ENABLE_TESTING_TRIGGERS = True

    UPLOADED_DEFAULT_DEST = project_path() + 'static/images'
    UPLOADED_DEFAULT_URL = '/static/photos/'

    UPLOADED_IMAGES_DEST = project_path() + 'static/images'
    UPLOADED_IMAGES_URL = '/static/photos/'

    LOG_FILE = "/tmp/passport.log"
    LOG_LEVEL = logging.DEBUG

    OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 3600

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/passport.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_POST_LOGIN_VIEW = 'auth/register'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'

    JWT_PRIVATE_KEY = project_path() + '/resources/test_rsa_private_key.txt'
    JWT_PUBLIC_KEY = project_path() + '/resources/test_rsa_public_key.txt'
    JWT_ALGORITHM = 'RS256'
