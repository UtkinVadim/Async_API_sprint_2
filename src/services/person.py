from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from services.base_service import BaseService, RedisCacher, ElasticSearcher
from services.utils import key_generator


class PersonService(BaseService):
    def __init__(self, redis: RedisCacher, elastic: ElasticSearcher, key_generator: key_generator):
        super().__init__(redis, elastic, key_generator)
        self.index = "person"
        self.model = Person


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(RedisCacher(redis), ElasticSearcher(elastic), key_generator)