import redis
import redis.asyncio as aioredis
import json
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


def get_cached_data(key):
    data = redis_client.get(key)
    return json.loads(data) if data else None


def set_cached_data(key, data, expire=3600):
    redis_client.setex(key, expire, json.dumps(data))


async def get_cached_data_async(key):
    data = await async_redis_client.get(key)
    return json.loads(data) if data else None


async def set_cached_data_async(key, data, expire=3600):
    await async_redis_client.setex(key, expire, json.dumps(data))
