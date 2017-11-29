from datetime import datetime, timedelta
from werkzeug.security import gen_salt

from ...extensions import db, oauth
from ...models import Client, Grant

from ..users.service import current_user


def list_clients(client_id=None):
    query = Client.query
    query = query.filter_by(id=client_id) if client_id else query
    return query.all()
    

def create_client_credentials(client, persist_to_db=True):
    client.client_id=gen_salt(40)
    client.client_secret=gen_salt(50)
    
    if persist_to_db:
        client._default_scopes='email'
        client.user_id=1
        db.session.add(client)
        db.session.commit()

    return client


def reset_credentials(name):
    client = Client.query.filter_by(name=name).first()
    client = create_client_credentials(client)
    db.session.commit()
    return create_credentials_response(client)


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
    grant = Grant.query.filter_by(client_id=client_id, code=code).first()
    return grant


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    expires = datetime.utcnow() + timedelta(seconds=600)
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
