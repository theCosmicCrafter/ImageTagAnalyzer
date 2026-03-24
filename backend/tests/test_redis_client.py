import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import json
import sys
import os

# Add backend directory to sys.path to allow importing from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock all dependencies of app.redis_client before importing it
mock_settings = MagicMock()
mock_settings.REDIS_HOST = 'localhost'
mock_settings.REDIS_PORT = 6379

sys.modules['app.config'] = MagicMock()
sys.modules['app.config'].settings = mock_settings
sys.modules['redis'] = MagicMock()
sys.modules['redis.asyncio'] = MagicMock()

import app.redis_client

class TestRedisClientSync(unittest.TestCase):
    def setUp(self):
        # Reset mocks before each test
        from app.redis_client import redis_client
        redis_client.reset_mock()

    def test_set_cached_data_sync(self):
        from app.redis_client import set_cached_data_sync, redis_client

        key = "test_key"
        data = {"foo": "bar"}
        expire = 100

        set_cached_data_sync(key, data, expire)

        redis_client.setex.assert_called_once_with(key, expire, json.dumps(data))

    def test_get_cached_data_sync(self):
        from app.redis_client import get_cached_data_sync, redis_client

        key = "test_key"
        data = {"foo": "bar"}
        redis_client.get.return_value = json.dumps(data)

        result = get_cached_data_sync(key)

        redis_client.get.assert_called_once_with(key)
        self.assertEqual(result, data)

    def test_get_cached_data_sync_none(self):
        from app.redis_client import get_cached_data_sync, redis_client

        key = "missing_key"
        redis_client.get.return_value = None

        result = get_cached_data_sync(key)

        self.assertIsNone(result)

class TestRedisClientAsync(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        from app.redis_client import async_redis_client
        async_redis_client.reset_mock()
        # Ensure methods are AsyncMocks
        async_redis_client.get = AsyncMock()
        async_redis_client.setex = AsyncMock()

    async def test_set_cached_data_async_explicit(self):
        from app.redis_client import set_cached_data_async, async_redis_client

        key = "async_key"
        data = {"async": "data"}
        expire = 200

        await set_cached_data_async(key, data, expire)

        async_redis_client.setex.assert_awaited_once_with(key, expire, json.dumps(data))

    async def test_get_cached_data_async_explicit(self):
        from app.redis_client import get_cached_data_async, async_redis_client

        key = "async_key"
        data = {"async": "data"}
        async_redis_client.get.return_value = json.dumps(data)

        result = await get_cached_data_async(key)

        async_redis_client.get.assert_awaited_once_with(key)
        self.assertEqual(result, data)

    async def test_set_cached_data_alias(self):
        from app.redis_client import set_cached_data, async_redis_client

        key = "alias_key"
        data = {"alias": "data"}
        expire = 300

        await set_cached_data(key, data, expire)

        async_redis_client.setex.assert_awaited_once_with(key, expire, json.dumps(data))

    async def test_get_cached_data_alias(self):
        from app.redis_client import get_cached_data, async_redis_client

        key = "alias_key"
        data = {"alias": "data"}
        async_redis_client.get.return_value = json.dumps(data)

        result = await get_cached_data(key)

        async_redis_client.get.assert_awaited_once_with(key)
        self.assertEqual(result, data)

if __name__ == '__main__':
    unittest.main()
