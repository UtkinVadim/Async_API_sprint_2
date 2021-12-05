import json
import pytest


@pytest.mark.asyncio
async def test_all_persons(make_get_request):
    response = await make_get_request(method="/person/search", params={"query": "Person"})
    assert response.status == 200, response.body
    assert len(response.body) == 3, response.body
    expected = [
        {"uuid": "1", "full_name": "Person 1", "films": [{"1": "role 1"}]},
        {"uuid": "2", "full_name": "Person 2", "films": [{"2": "role 2"}]},
        {"uuid": "3", "full_name": "Person 3", "films": [{"3": "role 3"}]},
    ]
    assert response.body == expected


@pytest.mark.asyncio
async def test_person_not_found(make_get_request):
    response = await make_get_request(method="/person/search", params={"query": "good_modern_russian_actor"})
    assert response.status == 404, response.body
    expected = {"detail": "person not found"}
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_specific_person(make_get_request):
    response = await make_get_request(method="/person/1")
    assert response.status == 200, response.body
    expected = {"uuid": "1", "full_name": "Person 1", "films": [{"1": "role 1"}]}
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_person_films(make_get_request):
    response = await make_get_request(method="/person/1/film")
    assert response.status == 200, response.body
    expected = [{"uuid": "1", "title": "film 1", "imdb_rating": 1.0}]
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_person_from_redis_cache(make_get_request, redis_client):
    personfilms = [
        {"id": "1", "title": "Хоббит: Нежданное путешествие", "imdb_rating": 9, "role": "Хоббит"},
        {"id": "2", "title": "Хоббит: Пустошь Смауга", "imdb_rating": 8, "role": "Хоббит"},
        {"id": "3", "title": "Хоббит: Битва пяти воинств", "imdb_rating": 10, "role": "Хоббит"}
    ]
    person = json.dumps({"id": "hobbit_id", "fullname": "Bilbo Baggins", "film_ids": personfilms})
    await redis_client.set("person::hobbit_id", person)
    response = await make_get_request(method="/person/hobbit_id")

    assert response.status == 200

    expected = {
        "uuid": "hobbit_id",
        "full_name": "Bilbo Baggins",
        "films": [
            {"1": "Хоббит"},
            {"2": "Хоббит"},
            {"3": "Хоббит"}
        ]
    }

    assert response.body == expected


@pytest.mark.asyncio
async def test_person_not_found_in_elastic(make_get_request):
    response = await make_get_request(method="/person/good_modern_russian_actor")
    assert response.status == 404, response.body
    expected = {"detail": {"_index": "person", "_type": "_doc", "_id": "good_modern_russian_actor", "found": False}}
    assert response.body == expected
