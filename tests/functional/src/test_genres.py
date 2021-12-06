import json

import pytest


@pytest.mark.asyncio
async def test_all_genres(make_get_request):
    response = await make_get_request(method="/genre/")
    assert response.status == 200, response.body
    assert len(response.body) == 20, response.body
    expected = [
        {"uuid": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
        {"uuid": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"},
        {"uuid": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Fantasy"},
        {"uuid": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
        {"uuid": "1cacff68-643e-4ddd-8f57-84b62538081a", "name": "Drama"},
        {"uuid": "56b541ab-4d66-4021-8708-397762bff2d4", "name": "Music"},
        {"uuid": "237fd1e4-c98e-454e-aa13-8a13fb7547b5", "name": "Romance"},
        {"uuid": "526769d7-df18-4661-9aa6-49ed24e9dfd8", "name": "Thriller"},
        {"uuid": "ca88141b-a6b4-450d-bbc3-efa940e4953f", "name": "Mystery"},
        {"uuid": "6a0a479b-cfec-41ac-b520-41b2b007b611", "name": "Animation"},
        {"uuid": "55c723c1-6d90-4a04-a44b-e9792040251a", "name": "Family"},
        {"uuid": "ca124c76-9760-4406-bfa0-409b1e38d200", "name": "Biography"},
        {"uuid": "9c91a5b2-eb70-4889-8581-ebe427370edd", "name": "Musical"},
        {"uuid": "63c24835-34d3-4279-8d81-3c5f4ddb0cdc", "name": "Crime"},
        {"uuid": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395", "name": "Short"},
        {"uuid": "0b105f87-e0a5-45dc-8ce7-f8632088f390", "name": "Western"},
        {"uuid": "6d141ad2-d407-4252-bda4-95590aaf062a", "name": "Documentary"},
        {"uuid": "eb7212a7-dd10-4552-bf7b-7a505a8c0b95", "name": "History"},
        {"uuid": "c020dab2-e9bd-4758-95ca-dbe363462173", "name": "War"},
        {"uuid": "e508c1c8-24c0-4136-80b4-340c4befb190", "name": "Reality-TV"},
    ]
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_specific_genre(make_get_request, es_client):
    response = await make_get_request(method="/genre/120a21cf-9097-479e-904a-13dd7198c1dd")
    assert response.status == 200
    expected = {"uuid": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"}
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
