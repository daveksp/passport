from flask import request
from flask_oauthlib.utils import extract_params

from ...extensions import oauth


def authorize(self, *args, **kwargs):
    """When consumer confirm the authorization."""

    server = oauth.server
    scope = request.values.get('scope') or ''
    scopes = scope.split()
    credentials = dict(
        client_id=request.values.get('client_id'),
        redirect_uri=request.values.get('redirect_uri', None),
        response_type=request.values.get('response_type', None),
        state=request.values.get('state', None)
    )

    uri, http_method, body, headers = extract_params()
    request.client_id = credentials['client_id']
    ret = server.create_authorization_response(
        uri, http_method, body, headers, scopes, credentials)
    import pdb; pdb.set_trace()
    return ret
