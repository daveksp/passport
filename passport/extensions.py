from flask_celeryext import FlaskCeleryExt
from flask_security import Security
from flask_kvsession import KVSessionExtension
from flask_oauthlib.provider import OAuth2Provider
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES
from simplekv.memory.redisstore import RedisStore
import redis

from sentinel import Authorizer


store = RedisStore(redis.StrictRedis())

db = SQLAlchemy()

oauth = OAuth2Provider()

celery = FlaskCeleryExt()

security = Security()

images = UploadSet('images', IMAGES)

sentinel = Authorizer()
