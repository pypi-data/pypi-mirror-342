from .connection import RedisInstance


def is_redis_connected(redis: RedisInstance) -> tuple[bool, Exception | None]:
    try:
        return redis.get_redis_client().ping(), None
    except Exception as e:
        return False, e
