from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.base_service import BaseService, RedisCacher, ElasticSearcher
from services.utils import key_generator


class GenreService(BaseService):
    def __init__(self, redis: RedisCacher, elastic: ElasticSearcher, key_generator: key_generator):
        super().__init__(redis, elastic, key_generator)
        self.index = "genre"
        self.model = Genre


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(RedisCacher(redis), ElasticSearcher(elastic), key_generator)
