from app.redis import redis_db
import json


def get_from_redis(key):
    return json.loads(redis_db.get(key))


def write_to_redis(key, value):
    redis_db.set(key, json.dumps(value))


def exists_in_redis(key):
    return redis_db.exists(key)
