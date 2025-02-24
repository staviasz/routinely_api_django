import pytest
import time
from main.configs.redis_client import redis_client
from modules.customer.infra.cache.cache import Cache


class TestCache:
    @pytest.fixture(scope="function", autouse=True)
    def setup_and_teardown(self):
        redis_client.flushdb()
        self.cache = Cache()
        yield
        redis_client.flushdb()

    def test_set_and_get(self):
        self.cache.set("test_key", "test_value")
        result = self.cache.get("test_key")

        assert result == "test_value"

    def test_get_non_existing_key(self):
        result = self.cache.get("missing_key")

        assert result is None

    def test_key_expiration(self):
        self.cache.set("test_key", "test_value")

        ttl = redis_client.ttl("test_key")
        assert ttl <= 600
        time.sleep(1)
        new_ttl = redis_client.ttl("test_key")
        assert new_ttl < ttl

    def test_key_expires_after_time(self):
        self.cache.set("test_key", "test_value")

        time.sleep(0.5)
        redis_client.expire("test_key", 1)
        time.sleep(1.2)

        result = self.cache.get("test_key")
        assert result is None
