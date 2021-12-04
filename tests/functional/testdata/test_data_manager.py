from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from functional.testdata.elastic_test_data_manager import ElasticTestDataManager
from functional.testdata.redis_test_data_manager import RedisTestDataManager


class TestDataManager(ElasticTestDataManager, RedisTestDataManager):
    def __init__(self, elastic_client: AsyncElasticsearch, redis_client: Redis):
        ElasticTestDataManager.__init__(self, elastic_client=elastic_client)
        RedisTestDataManager.__init__(self, redis_client=redis_client)

    async def create_test_data(self):
        await self.create_elastic_test_data()

    async def delete_test_data(self):
        await self.delete_elastic_test_data()
        # await self.clear_redis_cache()
