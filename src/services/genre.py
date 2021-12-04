from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.base_service import BaseService
from services.cacher import RedisCacher
from services.searcher import ElasticSearcher


class GenreService(BaseService):
    def __init__(self, redis: RedisCacher, elastic: ElasticSearcher):
        super().__init__(redis, elastic)
        self.index = "genre"
        self.model = Genre


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(RedisCacher(redis), ElasticSearcher(elastic))
