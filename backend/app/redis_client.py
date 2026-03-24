import json
import redis
import redis.asyncio as aioredis
from app.config import settings

# Sync client
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    # password=settings.REDIS_PASSWORD,
    decode_responses=True,
)

# Async client
async_redis_client = aioredis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    # password=settings.REDIS_PASSWORD,
    decode_responses=True,
)


async def get_cached_data_async(key):
    data = await async_redis_client.get(key)
    return json.loads(data) if data else None


async def set_cached_data_async(key, data, expire=3600):
    await async_redis_client.setex(key, expire, json.dumps(data))


# Aliases for async versions to maintain compatibility
get_cached_data = get_cached_data_async
set_cached_data = set_cached_data_async


def get_cached_data_sync(key):
    data = redis_client.get(key)
    return json.loads(data) if data else None


def set_cached_data_sync(key, data, expire=3600):
    redis_client.setex(key, expire, json.dumps(data))
