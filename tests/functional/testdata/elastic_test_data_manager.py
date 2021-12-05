import json
from pathlib import Path

from elasticsearch import AsyncElasticsearch


class ElasticTestDataManager:
    def __init__(self, elastic_client: AsyncElasticsearch):
        self.elastic_client = elastic_client
        self.test_data_path = Path(__file__).resolve().parent

    async def create_elastic_test_data(self):
        await self._create_indexes()
        await self._create_test_data()

    async def _create_indexes(self):
        await self._create_index(index="genre", settings_path=f"{self.test_data_path}/genre_index_settings.json")
        await self._create_index(index="person", settings_path=f"{self.test_data_path}/person_index_settings.json")
        await self._create_index(index="movies", settings_path=f"{self.test_data_path}/film_index_settings.json")

    async def _create_test_data(self):
        await self.elastic_client.bulk(
            body=[
                {"index": {"_index": "genre", "_id": "1"}},
                {"id": "1", "name": "Action"},
                {"index": {"_index": "genre", "_id": "2"}},
                {"id": "2", "name": "Comedy"},
                {"index": {"_index": "genre", "_id": "3"}},
                {"id": "3", "name": "AbraCadabra"},
                {"index": {"_index": "person", "_id": "1"}},
                {
                    "id": "1",
                    "fullname": "Person 1",
                    "film_ids": [{"id": "1", "title": "film 1", "imdb_rating": 1, "role": "role 1"}],
                },
                {"index": {"_index": "person", "_id": "2"}},
                {
                    "id": "2",
                    "fullname": "Person 2",
                    "film_ids": [{"id": "2", "title": "film 2", "imdb_rating": 2, "role": "role 2"}],
                },
                {"index": {"_index": "person", "_id": "3"}},
                {
                    "id": "3",
                    "fullname": "Person 3",
                    "film_ids": [{"id": "3", "title": "film 3", "imdb_rating": 3, "role": "role 3"}],
                },
            ],
            refresh=True,
        )

    async def _create_index(self, settings_path: str, index: str):
        with open(settings_path, "r") as settings:
            await self.elastic_client.indices.create(index=index, ignore=400, body=json.loads(settings.read()))

    async def delete_elastic_test_data(self):
        await self.elastic_client.indices.delete(index="*", ignore=[400, 404])
