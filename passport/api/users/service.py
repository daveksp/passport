from flask import session

from ...extensions import images
from ...models import User


def save_photo(image, username):
    filename = image.filename
    saved_photo = images.save(image, name=filename + username)
    photo_url = images.url(saved_photo)

    return photo_url


def current_user():
    if 'user_id' in session:
        uid = session['user_id']
        return User.query.get(uid)
    return None
