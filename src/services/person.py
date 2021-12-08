from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from models.person import Person
from services.base_service import BaseService
from services.cacher import Cacher, get_redis_extended
from services.searcher import Searcher


class PersonService(BaseService):
    def __init__(self, cacher: Cacher, searcher: Searcher):
        super().__init__(cacher, searcher)
        self.index = "person"
        self.model = Person


@lru_cache()
def get_person_service(
    cache_engine: Cacher = Depends(get_redis_extended),
    search_engine: Searcher = Depends(get_elastic),
) -> PersonService:
    return PersonService(cacher=cache_engine, searcher=search_engine)
