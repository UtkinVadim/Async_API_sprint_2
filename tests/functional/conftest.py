from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from functional import settings
from functional.testdata.test_data_manager import TestDataManager
from multidict import CIMultiDictProxy

SERVICE_URL = "http://127.0.0.1:8000"


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
async def es_client():
    client = AsyncElasticsearch(hosts=f"{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}")
    yield client
    await client.close()


@pytest.fixture
async def redis_client():
    redis = await aioredis.create_redis_pool((settings.REDIS_HOST, settings.REDIS_PORT), minsize=10, maxsize=20)
    yield redis
    await redis.flushall(async_op=True)
    redis.close()
    await redis.wait_closed()


@pytest.fixture
async def session(es_client, redis_client):
    session = aiohttp.ClientSession()
    test_data_manager = TestDataManager(elastic_client=es_client)
    await test_data_manager.create_test_data()
    yield session
    # await test_data_manager.delete_test_data()
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + "/api/v1" + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
