import pkgutil
import importlib

from flask import Blueprint


def register_blueprints(app, package_name, package_path):
    """Register all :class:`~flask.Blueprint` instances on the app."""
    for _, name, _ in pkgutil.iter_modules(package_path):
        module = importlib.import_module('{}.{}'.format(package_name, name))
        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
