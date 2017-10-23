from datetime import datetime, timedelta

from ...extensions import db, jwt, oauth, store
from ...models import Token
from ..persons.service import generate_jwt


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)
    if 'refresh_token' not in token:
        token['refresh_token'] = ''

    token_obj = Token(
        access_token=token['access_token'],
        #refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(token_obj)
    db.session.commit()
    token = generate_jwt(request.user)
    store.put(token_obj.access_token,  str(token))
    return token_obj


def remove_expired_tokens():
    tokens = Token.query.filter(
        Token.expires < datetime.utcnow()).all()

    for token in tokens:
        store.delete(token.access_token)
        db.session.delete(token)
        db.session.commit()
