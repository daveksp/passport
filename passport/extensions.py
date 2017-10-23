from flask_celeryext import FlaskCeleryExt
from flask.ext.security import Security
from flask_kvsession import KVSessionExtension
from flask_migrate import Migrate
from flask_oauthlib.provider import OAuth2Provider
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES
from simplekv.memory.redisstore import RedisStore
import redis

from jwt import JWTAuthenticator


store = RedisStore(redis.StrictRedis())

db = SQLAlchemy()

migrate = Migrate()

oauth = OAuth2Provider()

celery = FlaskCeleryExt()

security = Security()

images = UploadSet('images', IMAGES)

jwt = JWTAuthenticator()

kv_session = KVSessionExtension(store)
