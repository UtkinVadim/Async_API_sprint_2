import logging
from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film
from services.base_service import BaseService, ElasticSearcher, RedisCacher
from services.utils import key_generator

logger = logging.getLogger(__name__)


class FilmService(BaseService):
    def __init__(self, redis: RedisCacher, elastic: ElasticSearcher, key_generator: key_generator):
        super().__init__(redis, elastic, key_generator)
        self.index = "movies"
        self.model = Film


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(RedisCacher(redis), ElasticSearcher(elastic), key_generator)
