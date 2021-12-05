import json
from pathlib import Path

from elasticsearch import AsyncElasticsearch, helpers


class ElasticTestDataManager:
    def __init__(self, elastic_client: AsyncElasticsearch = None):
        self.elastic_client = elastic_client
        self.test_data_path = Path(__file__).resolve().parent.parent / "testdata"

    async def create_elastic_test_data(self):
        """
        Метод для наполнения elasticsearch данными для тестов.
        """
        await self._create_indexes()
        await self._create_test_data()

    async def _create_indexes(self):
        """
        Метод для создания индексов в elasticsearch.
        """
        await self._create_index(index="genre", settings_path=f"{self.test_data_path}/genre_index_settings.json")
        await self._create_index(index="person", settings_path=f"{self.test_data_path}/person_index_settings.json")
        await self._create_index(index="movies", settings_path=f"{self.test_data_path}/film_index_settings.json")

    async def _create_test_data(self):
        """
        Метод для создания записей в elasticsearch.
        """
        await self._create_test_data_from_file(data_path=f"{self.test_data_path}/films_data.json", index="movies")
        await self._create_test_data_from_file(data_path=f"{self.test_data_path}/genres_data.json", index="genre")
        await self._create_test_data_from_file(data_path=f"{self.test_data_path}/persons_data.json", index="person")

    async def _create_test_data_from_file(self, data_path: str, index: str):
        """
        Метод для наполнения индекса данными, прочитанными из файла.
        :param index: имя индекса в который будут загружены данные.
        :param data_path: Путь к json файлу с данными, которые нужно загрузить.
        """
        with open(data_path, "r") as films_data:
            await helpers.async_bulk(client=self.elastic_client,
                                     actions=json.load(films_data),
                                     index=index,
                                     refresh=True)

    async def _create_index(self, settings_path: str, index: str):
        """
        Метод для наполнения индекса данными, прочитанными из файла.
        :param index: Имя создаваемого индекса.
        :param settings_path: Путь к json файлу с настройками создаваемого индекса.
        """
        with open(settings_path, "r") as index_settings_file:
            index_settings = json.loads(index_settings_file.read())
            await self.elastic_client.indices.create(index=index,
                                                     settings=index_settings["settings"],
                                                     mappings=index_settings["mappings"],
                                                     ignore=400)

    async def delete_elastic_test_data(self):
        """
        Метод для удаления всех индексов из elasticsearch.
        """
        await self.elastic_client.indices.delete(index="person", ignore=[400, 404])
        await self.elastic_client.indices.delete(index="genre", ignore=[400, 404])
        await self.elastic_client.indices.delete(index="movies", ignore=[400, 404])
