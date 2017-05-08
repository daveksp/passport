from datetime import datetime, timedelta

from ...extensions import db, oauth
from ...models import Token


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

    token_obj = Token(
        access_token=token['access_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(token_obj)
    db.session.commit()
    return token_obj


def remove_expired_tokens():
    tokens = Token.query.filter(
        Token.expires < datetime.utcnow()).all()

    for token in tokens:
        db.session.delete(token)
        db.session.commit()
