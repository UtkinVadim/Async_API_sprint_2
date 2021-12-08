import logging
from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from models.genre import Genre
from services.base_service import BaseService
from services.cacher import Cacher
from services.searcher import Searcher

logger = logging.getLogger(__name__)


class FilmService(BaseService):
    def __init__(self, cacher: Cacher, searcher: Searcher):
        super().__init__(cacher, searcher)
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
    cache_engine: Cacher = Depends(get_redis),
    search_engine: Searcher = Depends(get_elastic),
) -> FilmService:
    return FilmService(cacher=cache_engine, searcher=search_engine)
