from datetime import datetime, timedelta
from werkzeug.security import gen_salt

from ..users.service import current_user

from ...extensions import db, oauth
from ...models import Client, Grant


def create_client(name, redirect_uris):
    # 'http://localhost:8000/authorized'
    client = Client(
        name=name,
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=redirect_uris,
        _default_scopes='email',
    )
    db.session.add(client)
    db.session.commit()

    return client


def reset_credentials(name):
    client = Client.query.filter_by(name=name).first()
    db.session.delete(client)
    new_client = create_client(client.name, client._redirect_uris)
    db.session.commit()
    return create_credentials_response(new_client)


def create_credentials_response(client):
    return {
        'client_id': client.client_id,
        'client_secret': client.client_secret
    }


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.now() + timedelta(sec=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_user(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant
