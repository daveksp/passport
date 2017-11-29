from flask import session

from ...extensions import db, images, sentinel
from ...models import User
from .schema import UserSchema

user_schema = UserSchema()


def user_schema_load(json):
    return user_schema.load(json or {})[0]


def user_schema_dump(person):
    return user_schema.dump(person)[0]


def save_and_dump_user(user):
    db.session.add(user)
    db.session.commit()

    return user_schema_dump(user)

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

def generate_jwt(user):
    user = User.query.filter_by(id=user.id).first()
    schema = UserSchema()
    response, response_errors = schema.dump(user)
    token = sentinel.authorize(response)

    return token
