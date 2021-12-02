import json
from abc import ABC, abstractmethod
from typing import Optional, Union, List

from aioredis import Redis
from pydantic import BaseModel

from core.config import CACHE_EXPIRE_IN_SECONDS


class Cacher(ABC):
    @abstractmethod
    async def get(self):
        """ Метод взятия объекта из кэша """

    @abstractmethod
    async def put(self):
        """ Метод пишущий объект (или группу объектов) в кэш """

    @classmethod
    async def flatten_json(cls, obj) -> List:
        """
        "Плющит" входной объект.

        Пример работы:
        {'a': {'b': 'c'}} -> ['a', 'b', 'c']

        :param obj:
        :return:
        """
        body_list = []

        async def flatten(x):
            if isinstance(x, dict):
                for a in x:
                    body_list.append(a)
                    await flatten(x[a])
            elif isinstance(x, list):
                for a in x:
                    await flatten(a)
            else:
                body_list.append(x)

        await flatten(obj)
        return body_list

    @classmethod
    async def key_generator(cls, index: str, body: Union[dict, str]) -> str:
        """
        Создаёт ключ для редиса, по которому будут храниться данные.
        Структура ключа:
        <es_index>::<first_key>::<first_value>::<second_key>::<second_value>

        :param index:
        :param body:
        :return:
        """

        body_list = await cls.flatten_json(body)
        keys_list = [index, *body_list]
        separate_symbol = "::"
        key = separate_symbol.join(keys_list)

        return key


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