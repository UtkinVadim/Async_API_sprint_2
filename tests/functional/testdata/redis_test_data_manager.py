from aioredis import Redis


class RedisTestDataManager:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def clear_redis_cache(self):
        pass

        # for key in self.redis_client.scan("prefix:*"):
        #     self.redis_client.delete(key)
