import json
import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import List, Optional, Union

from aioredis import Redis
from core.config import CACHE_EXPIRE_IN_SECONDS
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import HTTPException
from pydantic import BaseModel

from .utils import key_generator

logger = logging.getLogger(__name__)


class Searcher(ABC):
    @abstractmethod
    async def get_by_id(self):
        """ Метод взятия объекта по id из базы """

    @abstractmethod
    async def search(self):
        """ Метод для поиска объектов в базе """


class Cacher(ABC):
    @abstractmethod
    async def get(self):
        """ Метод взятия объекта из кэша """

    @abstractmethod
    async def put(self):
        """ Метод пишущий объект (или группу объектов) в кэш """


class ElasticSearcher(Searcher):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, id_: str, index: str, model: BaseModel) -> Optional[BaseModel]:
        """
        Забирает данные из эластика по id. Результат валидируется моделью.

        :param id_:
        :return:
        """
        try:
            doc = await self.elastic.get(index, id_)
            return model(**doc["_source"])
        except NotFoundError as err:
            logger.exception("Ошибка на этапе забора документа из searcher по id")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err.info)
        except Exception as err:
            logger.warning(err, exc_info=True)
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=err)

    async def search(self, body: dict, index: str, model: BaseModel) -> Optional[List[BaseModel]]:
        """
        Выполяет поиск в индексе эластика index по запросу body.
        Возвращаемый результат валидируется моделью.

        :param body:
        :return:
        """
        docs = await self.elastic.search(index=index, body=body)
        docs = docs.get("hits", {})
        docs = docs.get("hits", [])
        docs = [model(**data["_source"]) for data in docs]
        return docs


class RedisCacher(Cacher):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str, model: BaseModel) -> Optional[BaseModel]:
        """
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        # pydantic предоставляет удобное API для создания объекта моделей из json

        :param key:
        :return:
        """
        data = await self.redis.get(key)
        if not data:
            return None

        if 'result' in json.loads(data).keys():
            data = json.loads(data)["result"]
            obj = [model.parse_raw(d) for d in data]
        else:
            obj = model.parse_raw(data)
        return obj

    async def put(
            self,
            obj: Union[BaseModel, List[BaseModel]],
            key: str,
    ) -> None:
        """
        Сохраняем данные, используя команду set
        Выставляем время жизни кеша — 5 минут
        https://redis.io/commands/set
        pydantic позволяет сериализовать модель в json

        :param obj:
        :return:
        """

        if isinstance(obj, list):
            data_to_cache = json.dumps({"result": [d.json() for d in obj]})
        else:
            data_to_cache = obj.json()

        await self.redis.set(key, data_to_cache, expire=CACHE_EXPIRE_IN_SECONDS)


class BaseService:
    def __init__(self, cacher: Cacher, searcher: Searcher, key_generator: key_generator):
        self.cacher = cacher
        self.searcher = searcher
        self.key_generator = key_generator
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
        key = await self.key_generator(index, id_)
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
        key = await self.key_generator(self.index, body)
        docs = await self.cacher.get(key, self.model)
        if not docs:
            docs = await self.searcher.search(body=body, index=self.index, model=self.model)
            if not docs:
                return None
            await self.cacher.put(docs, key=key)

        return docs
