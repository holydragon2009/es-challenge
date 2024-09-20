import redis

from app.core.config import REDIS_HOST, REDIS_PORT


def cache():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
    ).hset()
