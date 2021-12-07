import json
import pytest

from functional.utils.expected_data_parser import ExpectedDataParser

expected_data_parser = ExpectedDataParser()


@pytest.mark.asyncio
async def test_all_persons(make_get_request):
    response = await make_get_request(method="/person/search", params={"page[size]": "999"})
    assert response.status == 200, response.body
    assert len(response.body) == 20, response.body
    expected_data = await expected_data_parser.get_expected_persons_data()
    assert response.body == expected_data


@pytest.mark.asyncio
async def test_person_not_found(make_get_request):
    response = await make_get_request(method="/person/search", params={"query": "good_modern_russian_actor"})
    assert response.status == 404, response.body
    expected = {"detail": "person not found"}
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_specific_person(make_get_request):
    person_id = "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1"
    response = await make_get_request(method=f"/person/{person_id}")
    assert response.status == 200, response.body
    expected = await expected_data_parser.get_expected_persons_data(person_id=person_id)
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_person_films(make_get_request):
    person_id = "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1"
    response = await make_get_request(method=f"/person/{person_id}/film")
    assert response.status == 200, response.body
    assert len(response.body) == 11
    expected = await expected_data_parser.get_expected_person_film_data(person_id)
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_person_from_redis_cache(make_get_request, redis_client):
    personfilms = [
        {"id": "1", "title": "Хоббит: Нежданное путешествие", "imdb_rating": 9, "role": "Хоббит"},
        {"id": "2", "title": "Хоббит: Пустошь Смауга", "imdb_rating": 8, "role": "Хоббит"},
        {"id": "3", "title": "Хоббит: Битва пяти воинств", "imdb_rating": 10, "role": "Хоббит"},
    ]
    person = json.dumps({"id": "hobbit_id", "fullname": "Bilbo Baggins", "film_ids": personfilms})
    await redis_client.set("person::hobbit_id", person)
    response = await make_get_request(method="/person/hobbit_id")

    assert response.status == 200

    expected = {"uuid": "hobbit_id", "full_name": "Bilbo Baggins", "films": [{"1": "Хоббит"}, {"2": "Хоббит"}, {"3": "Хоббит"}]}

    assert response.body == expected


@pytest.mark.asyncio
async def test_person_not_found_in_elastic(make_get_request):
    response = await make_get_request(method="/person/good_modern_russian_actor")
    assert response.status == 404, response.body
    expected = {"detail": {"_index": "person", "_type": "_doc", "_id": "good_modern_russian_actor", "found": False}}
    assert response.body == expected
