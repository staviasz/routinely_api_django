from main.configs.redis_client import redis_client
from modules.customer.contracts import CacheContract


class Cache(CacheContract[str]):
    def __init__(self) -> None:
        self._cache = redis_client

    def get(self, key: str) -> str | None:
        return self._cache.get(key)

    def set(self, key: str, value: str) -> None:
        self._cache.setex(key, 600, value)
