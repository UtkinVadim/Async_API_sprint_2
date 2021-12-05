import json
import pytest


@pytest.mark.asyncio
async def test_all_genres(make_get_request):
    response = await make_get_request(method="/genre/")
    assert response.status == 200, response.body
    assert len(response.body) == 3, response.body
    expected = [{"uuid": "1", "name": "Action"}, {"uuid": "2", "name": "Comedy"}, {"uuid": "3", "name": "AbraCadabra"}]
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_specific_genre(make_get_request):
    response = await make_get_request(method="/genre/1")

    assert response.status == 200

    expected = {"uuid": "1", "name": "Action"}

    assert response.body == expected


@pytest.mark.asyncio
async def test_genre_no_found(make_get_request):
    response = await make_get_request(method="/genre/fake_genre")

    assert response.status == 404

    expected = {"detail": {"_index": "genre", "_type": "_doc", "_id": "fake_genre", "found": False}}

    assert response.body == expected


@pytest.mark.asyncio
async def test_find_from_redis_cache(make_get_request, redis_client):
    genre = json.dumps({"id": "genre_4", "name": "Genre from cache"})
    await redis_client.set("genre::genre_4", genre)
    response = await make_get_request(method="/genre/genre_4")

    assert response.status == 200

    expected = {"uuid": "genre_4", "name": "Genre from cache"}

    assert response.body == expected
