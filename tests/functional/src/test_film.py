import http
import json

import pytest
from functional.utils.expected_data_parser import ExpectedFilm

expected_data_parser = ExpectedFilm()


@pytest.mark.asyncio
async def test_film_detailed(make_get_request):
    film_id = "a7b11817-205f-4e1a-98b5-e3c48b824bc3"
    response = await make_get_request(method=f"/film/{film_id}")
    assert response.status == http.HTTPStatus.OK
    expected = await expected_data_parser.get_film_detailed_data(film_id=film_id)
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_detailed_not_found(make_get_request):
    response = await make_get_request(method="/film/Nonexistent_film")
    assert response.status == http.HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_film_filter(make_get_request):
    page_size = 5
    response = await make_get_request(method="/film", params={"page[size]": page_size})
    assert response.status == http.HTTPStatus.OK
    expected = await expected_data_parser.get_film_data(page_size=page_size)
    assert len(response.body) == page_size
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_filter_sorted_desc(make_get_request):
    page_size = 5
    sort = "-imdb_rating"
    response = await make_get_request(method="/film", params={"page[size]": page_size, "sort": sort})
    assert response.status == http.HTTPStatus.OK
    expected = await expected_data_parser.get_film_data(page_size=page_size, sort_by=sort)
    assert len(response.body) == page_size
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_filter_sorted_asc(make_get_request):
    genre_id = "ca88141b-a6b4-450d-bbc3-efa940e4953f"
    page_size = 3
    sort = "imdb_rating"
    response = await make_get_request(
        method="/film", params={"filter[genre]": genre_id, "page[size]": page_size, "sort": sort}
    )
    assert response.status == http.HTTPStatus.OK
    expected = await expected_data_parser.get_film_data(genre_id=genre_id, page_size=page_size, sort_by=sort)
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_filter_paginator(make_get_request):
    genre_id = "6c162475-c7ed-4461-9184-001ef3d9f26e"
    page_size = 3
    page_number = 2
    sort = "imdb_rating"
    response = await make_get_request(
        method="/film",
        params={"filter[genre]": genre_id, "page[size]": page_size, "page[number]": page_number, "sort": sort},
    )
    assert response.status == http.HTTPStatus.OK
    expected = await expected_data_parser.get_film_data(
        genre_id=genre_id, page_size=page_size, page_number=page_number, sort_by=sort
    )
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_filter_all(make_get_request):
    page_size = 9999
    response = await make_get_request(method="/film", params={"page[size]": page_size})
    expected = await expected_data_parser.get_film_data(page_size=page_size)
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_filter_all_cached(make_get_request, redis_client):
    page_size = 9999
    response = await make_get_request(method="/film", params={"page[size]": page_size})
    expected = await expected_data_parser.get_film_data(page_size=page_size)
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected)
    assert response.body == expected

    cache_expected = [
        {
            "id": "3d825f60-9fff-4dfe-b294-1a45fa1e115e",
            "title": "test_title",
            "imdb_rating": 0,
        }
    ]

    cache = json.dumps({"result": [json.dumps(d) for d in cache_expected]})
    await redis_client.set("movies::query::bool::must::match_all::size::9999", cache)

    response = await make_get_request(method="/film", params={"page[size]": page_size})
    assert response.body == cache_expected
