import json
import logging
from typing import Iterable, Union, List

from elasticsearch import AsyncElasticsearch, helpers

log = logging.getLogger(__name__)


class ElasticWrapper:
    def __init__(self, hosts=None, **kwargs):
        self.client = AsyncElasticsearch(hosts, **kwargs)

    async def create_index(self, index_name, index_settings: Iterable,
                           ignore: Union[int, List[int], None] = 400) -> None:
        """
        Создаёт индекс в elastic с указанными настройками.

        :param index_name: имя индекса
        :param index_settings: словарь с настройками индекса
        :param ignore:
        :return:
        """
        await self.client.indices.create(index=index_name, body=index_settings, ignore=ignore)
        log.info(f"Index {index_name} created")

    async def create_index_from_file(self, index_name, index_settings_path: str,
                                     ignore: Union[int, List[int], None] = 400) -> None:
        """
        Создаёт индекс в elastic из json файла

        :param index_name:
        :param index_settings_path:
        :param ignore:
        :return:
        """
        with open(index_settings_path, 'r') as file:
            indx = json.load(file)
        await self.create_index(index_name=index_name, index_settings=indx, ignore=ignore)

    async def load(self, index_name: str, data: Iterable) -> None:
        """
        Загружает data данные в index_name elastic'а

        :param index_name:
        :param data:
        :return:
        """
        lines, _ = await helpers.async_bulk(client=self.client, actions=data, index=index_name)
        log.info(f"Lines recorded in elastic: {lines}")

    async def load_from_file(self, index_name: str, data_path: str) -> None:
        """
        Загружает data данные в index_name elastic'а

        :param index_name:
        :param data_path:
        :return:
        """
        with open(data_path, 'r') as file:
            data = json.load(file)
        await self.load(index_name=index_name, data=data)

    async def delete_index(self, index_name: str, ignore: Union[int, List[int], None] = [400, 404]) -> None:
        """
        Удаляет индекс из эластика
        """
        await self.client.indices.delete(index=index_name, ignore=ignore)
        log.info(f"Index {index_name} deleted")

    async def delete_data(self, index_name: str, ignore: Union[int, List[int], None] = [400, 404]) -> None:
        """
        Удаляет данные из индекса эластика
        """
        await self.client.delete_by_query(index=index_name, body={"query": {"match_all": {}}}, ignore=ignore)
        log.info(f"Data from index {index_name} deleted")

    async def close(self) -> None:
        """
        Закрывает соединение
        """
        await self.client.close()

