from flask import Flask
from flask_security import SQLAlchemyUserDatastore
from flask_uploads import configure_uploads

from .. import config
from ..api.utilities import project_path
from ..extensions import (celery, db, images, oauth, security, sentinel)
from ..models import User, Role
from ..security.login_form import ExtendedLoginForm

from .register_blueprints import register_blueprints
from .initialize_extensions import initialize_extensions
from .configure_logging import configure_logging


def create_app(package_name, package_path, settings_override=None,
               extensions=None, app=None):
    """Returns a :class:`Flask` application instance configured with common
    functionality for this application.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary or path to file of settings to
        override
    :param extensions: an array of instances of additional extensions to
        initialize on the app
    """
    app = Flask(package_name)
    
    app.config.from_object(config.Common())
    app.config.from_pyfile(project_path('settings.cfg'), silent=True)

    if isinstance(settings_override, basestring):
        app.config.from_pyfile(settings_override, silent=True)
    else:
        app.config.from_object(settings_override)

    common_extensions = frozenset([celery, db, oauth, sentinel])
    
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, login_form=ExtendedLoginForm)

    initialize_extensions(app, common_extensions)
    register_blueprints(app, package_name, package_path)
    initialize_extensions(app, extensions)

    configure_logging(app)
    configure_uploads(app, images)
    
    return app
