import uuid
import os

from flask import current_app, request, g


# Return an id that lasts the life of the request,
# or create one if this is the first time the value is being returned
def request_ids():
    if getattr(g, 'request_id', None):
        return g.request_id, g.get('original_request_id')

    g.request_id = _generate_request_id()
    g.original_request_id = request.headers.get("Request-Id")

    return g.request_id, g.original_request_id


# Generate a new request ID
def _generate_request_id():
    return uuid.uuid4()


# return the request endpoint
def get_request_endpoint():
    return request.url_rule.endpoint


def redact_sensitive_data(data, sensitive_fields):
    print(data)
    return dict((k, v) if k not in sensitive_fields else (k, '[redacted]')
                for k, v in data.iteritems())


def project_path(subpath=None):
    """
    Get project's absolute path

    :param subpath: A subpath within the project.  If omitted,
    return the project root
    """
    p = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if subpath:
        if isinstance(subpath, basestring):
            subpath = (subpath,)
        parts = (p,) + tuple(subpath)
        p = os.path.sep.join(parts)
    return p


def get_rsa_private_key():
    private_key = None
    with open(current_app.config['JWT_PRIVATE_KEY'], 'rb') as key_file:
        private_key = key_file.read()

    return private_key
