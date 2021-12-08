from typing import Optional

from aioredis import Redis

from services.cacher import RedisCacher

redis: Optional[Redis] = None


async def get_redis() -> RedisCacher:
    return RedisCacher(redis)
