import redis.asyncio as redis
import json
from app.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    # password=settings.REDIS_PASSWORD,
    decode_responses=True,
)


async def get_cached_data(key):
    data = await redis_client.get(key)
    return json.loads(data) if data else None


async def set_cached_data(key, data, expire=3600):
    await redis_client.setex(key, expire, json.dumps(data))
