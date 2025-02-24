import redis

from main.configs import env

redis_client = redis.Redis(
    host=env["queque"]["host"],
    port=env["queque"]["port"],
    decode_responses=True,
)
