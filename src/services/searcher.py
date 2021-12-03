import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Optional, List

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Searcher(ABC):
    @abstractmethod
    async def get_by_id(self):
        """ Метод взятия объекта по id из базы """

    @abstractmethod
    async def search(self):
        """ Метод для поиска объектов в базе """


class ElasticSearcher(Searcher):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, id_: str, index: str, model: BaseModel) -> Optional[BaseModel]:
        """
        Забирает данные из эластика по id. Результат валидируется моделью.

        :param id_:
        :param index:
        :param model:
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
        :param index:
        :param model:
        :return:
        """
        docs = await self.elastic.search(index=index, body=body)
        docs = docs.get("hits", {})
        docs = docs.get("hits", [])
        docs = [model(**data["_source"]) for data in docs]
        return docs