import http
import json

import pytest
from functional.utils.expected_data_parsers import ExpectedFilm, ExpectedPerson

expected_film_parser = ExpectedFilm()
expected_person_parser = ExpectedPerson()


@pytest.mark.asyncio
async def test_film_search_query(make_get_request):
    query = "war"
    page_size = 20
    response = await make_get_request(method="/film/search", params={"query": query, "page[size]": page_size})
    expected = await expected_film_parser.get_film_data(query=query, page_size=page_size)
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected)
    assert sorted(response.body, key=lambda x: x["id"]) == sorted(expected, key=lambda x: x["id"])


@pytest.mark.asyncio
async def test_film_search_filter(make_get_request):
    query = "trek"
    filter_genre_id = "ca88141b-a6b4-450d-bbc3-efa940e4953f"
    page_size = 20
    response = await make_get_request(
        method="/film/search",
        params={
            "query": query,
            "filter[genre]": filter_genre_id,
            "page[size]": page_size,
        },
    )
    expected = await expected_film_parser.get_film_data(query=query, page_size=page_size, genre_id=filter_genre_id)
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_search_sorted_desc(make_get_request):
    query = "trek"
    filter_genre_id = "ca88141b-a6b4-450d-bbc3-efa940e4953f"
    page_size = 20
    sort = "-imdb_rating"
    response = await make_get_request(
        method="/film/search",
        params={
            "query": query,
            "filter[genre]": filter_genre_id,
            "page[size]": page_size,
            "sort": sort,
        },
    )
    expected = await expected_film_parser.get_film_data(
        query=query, page_size=page_size, genre_id=filter_genre_id, sort_by=sort
    )
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_search_sorted_asc(make_get_request):
    query = "trek"
    filter_genre_id = "ca88141b-a6b4-450d-bbc3-efa940e4953f"
    page_size = 20
    sort = "imdb_rating"
    response = await make_get_request(
        method="/film/search",
        params={
            "query": query,
            "filter[genre]": filter_genre_id,
            "page[size]": page_size,
            "sort": sort,
        },
    )
    expected = await expected_film_parser.get_film_data(
        query=query, page_size=page_size, genre_id=filter_genre_id, sort_by=sort
    )
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_search_paginator(make_get_request):
    query = "trek"
    filter_genre_id = "ca88141b-a6b4-450d-bbc3-efa940e4953f"
    page_size = 1
    page_number = 2
    sort = "imdb_rating"
    response = await make_get_request(
        method="/film/search",
        params={
            "query": query,
            "filter[genre]": filter_genre_id,
            "page[size]": page_size,
            "page[number]": page_number,
            "sort": sort,
        },
    )
    expected = await expected_film_parser.get_film_data(
        query=query, page_size=page_size, page_number=page_number, genre_id=filter_genre_id, sort_by=sort
    )
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_person_search(make_get_request):
    query = "ford"
    response = await make_get_request(method="/person/search", params={"query": query})
    expected = await expected_person_parser.get_expected_persons_data(query=query)
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_person_search_cached(make_get_request, redis_client):
    query = "ford"
    response = await make_get_request(method="/person/search", params={"query": query})
    expected = await expected_person_parser.get_expected_persons_data(query=query)
    assert response.status == http.HTTPStatus.OK
    assert response.body == expected

    cache_expected = [{"id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "fullname": "some test name", "film_ids": []}]

    cache = json.dumps({"result": [json.dumps(d) for d in cache_expected]})
    await redis_client.set(f"person::query::bool::must::multi_match::query::{query}", cache)
    for person in cache_expected:
        person["uuid"] = person.pop("id")
        person["full_name"] = person.pop("fullname")
        person["films"] = person.pop("film_ids")

    response = await make_get_request(method="/person/search", params={"query": query})
    assert response.body == cache_expected
