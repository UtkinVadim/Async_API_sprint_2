import asyncio
from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
from functional import settings
from functional.utils.elastic_wrapper import ElasticWrapper
from multidict import CIMultiDictProxy

SERVICE_URL = 'http://127.0.0.1:8000'
indexes_dict = {'movies': '../testdata/film_index_settings.json',
                'genre': '../testdata/genre_index_settings.json',
                'person': '../testdata/person_index_settings.json',
                }

data_dict = {'movies': '../testdata/films_data.json',
             'genre': '../testdata/genres_data.json',
             'person': '../testdata/persons_data.json',
             }


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def es_client():
    client = ElasticWrapper(hosts=f"{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}")

    for index_name, index_path in indexes_dict.items():
        await client.create_index_from_file(index_name=index_name,
                                            index_settings_path=index_path)

    for index_name, data_path in data_dict.items():
        await client.load_from_file(index_name=index_name, data_path=data_path)

    yield client

    for index_name in indexes_dict.keys():
        await client.delete_data(index_name=index_name)
        await client.delete_index(index_name=index_name)

    await client.close()


@pytest.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis_pool((settings.REDIS_HOST, settings.REDIS_PORT), minsize=10, maxsize=20)
    yield redis
    await redis.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + '/api/v1' + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner
