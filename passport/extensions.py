from flask_celeryext import FlaskCeleryExt
from flask_security import Security
from flask_kvsession import KVSessionExtension
from flask_oauthlib.provider import OAuth2Provider
from flask_s3 import FlaskS3
from flask_sqlalchemy import SQLAlchemy
from simplekv.memory.redisstore import RedisStore
import redis

from sentinel import Authorizer


store = RedisStore(redis.StrictRedis())

db = SQLAlchemy()

oauth = OAuth2Provider()

celery = FlaskCeleryExt()

security = Security()

sentinel = Authorizer()

#s3 = FlaskS3()
