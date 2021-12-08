from elasticsearch import AsyncElasticsearch, helpers
from functional.utils.data_parser import DataParser


class ElasticTestDataManager(DataParser):
    def __init__(self, elastic_client: AsyncElasticsearch = None):
        super().__init__()
        self.elastic_client = elastic_client

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
        await self._create_index(index="genre", file_name="genre_index_settings.json")
        await self._create_index(index="person", file_name="person_index_settings.json")
        await self._create_index(index="movies", file_name="film_index_settings.json")

    async def _create_test_data(self):
        """
        Метод для создания записей в elasticsearch.
        """
        await self._create_test_data_from_file(file_name="films_data.json", index="movies")
        await self._create_test_data_from_file(file_name="genres_data.json", index="genre")
        await self._create_test_data_from_file(file_name="persons_data.json", index="person")

    async def _create_test_data_from_file(self, file_name: str, index: str):
        """
        Метод для наполнения индекса данными, прочитанными из файла.
        :param index: имя индекса в который будут загружены данные.
        :param file_name: Название json файла с данными, которые нужно загрузить.
        """
        actions = await self.get_data_from_file(file_name)
        await helpers.async_bulk(client=self.elastic_client, actions=actions, index=index, refresh=True)

    async def _create_index(self, file_name: str, index: str):
        """
        Метод для наполнения индекса данными, прочитанными из файла.
        :param index: Имя создаваемого индекса.
        :param file_name: Название json файла с настройками создаваемого индекса.
        """
        settings, mappings = await self.get_index_data_from_file(file_name)
        await self.elastic_client.indices.create(index=index, settings=settings, mappings=mappings, ignore=400)

    async def delete_elastic_test_data(self):
        """
        Метод для удаления всех индексов из elasticsearch.
        """
        await self.elastic_client.indices.delete(index="person", ignore=[400, 404])
        await self.elastic_client.indices.delete(index="genre", ignore=[400, 404])
        await self.elastic_client.indices.delete(index="movies", ignore=[400, 404])
