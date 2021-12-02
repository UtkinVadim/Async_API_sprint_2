from typing import List, Optional

from pydantic import BaseModel

from .cacher import Cacher
from .searcher import Searcher


class BaseService:
    def __init__(self, cacher: Cacher, searcher: Searcher):
        self.cacher = cacher
        self.searcher = searcher
        self.index = None
        self.model = None

    async def get_by_id(self, id_: str, index: str = None, model: Optional[BaseModel] = None) -> Optional[BaseModel]:
        """
        Возвращает объект по id из указанного индекса. Сначала ищет объект в кеше,
        при отсутствии: берёт из базы, кладёт в кеш, возвращает найденный объект.

        :param id_:
        :param index:
        :return:
        """
        index = index if index else self.index
        model = model if model else self.model
        key = await self.cacher.key_generator(index, id_)
        obj = await self.cacher.get(key, model)
        if not obj:
            obj = await self.searcher.get_by_id(id_, index, model=model)
            if not obj:
                return None
            await self.cacher.put(obj, key=key)
        return obj

    async def search(self, body: dict) -> Optional[List[BaseModel]]:
        """
        Выполняет поиск данных по запросу (body) и индексу. Сначала проверяет наличие данных в кеше.
        Если данных в кеше нет - обращается к БД и кеширует положительный результат.

        :param body:
        :return:
        """
        key = await self.cacher.key_generator(self.index, body)
        docs = await self.cacher.get(key, self.model)
        if not docs:
            docs = await self.searcher.search(body=body, index=self.index, model=self.model)
            if not docs:
                return None
            await self.cacher.put(docs, key=key)

        return docs
