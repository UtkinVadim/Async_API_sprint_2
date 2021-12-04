import logging
from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film
from models.genre import Genre
from services.base_service import BaseService
from services.cacher import RedisCacher
from services.searcher import ElasticSearcher

logger = logging.getLogger(__name__)


class FilmService(BaseService):
    def __init__(self, redis: RedisCacher, elastic: ElasticSearcher):
        super().__init__(redis, elastic)
        self.index = "movies"
        self.model = Film

    async def get_genre_by_id(self, id_: str):
        index = "genre"
        model = Genre
        key = await self.cacher.key_generator(index, id_)
        obj = await self.cacher.get(key, model)
        if not obj:
            obj = await self.searcher.get_by_id(id_, index, model=model)
            if not obj:
                return None
            await self.cacher.put(obj, key=key)
        return obj


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(RedisCacher(redis), ElasticSearcher(elastic))
