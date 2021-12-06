from elasticsearch import AsyncElasticsearch
from functional.utils.elastic_test_data_manager import ElasticTestDataManager


class TestDataManager(ElasticTestDataManager):
    def __init__(self, elastic_client: AsyncElasticsearch):
        ElasticTestDataManager.__init__(self, elastic_client=elastic_client)

    async def create_test_data(self):
        """
        Метод, для создания данных для тестов.
        """
        await self.create_elastic_test_data()

    async def delete_test_data(self):
        """
        Метод, для удаления тестовых данных.
        """
        await self.delete_elastic_test_data()
