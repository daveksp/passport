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
