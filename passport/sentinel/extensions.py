import redis
from simplekv.memory.redisstore import RedisStore

store = RedisStore(redis.StrictRedis())
