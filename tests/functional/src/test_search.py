import http
import json

import pytest
from functional.utils.expected_data_parser import ExpectedFilm

expected_data_parser = ExpectedFilm()


@pytest.mark.asyncio
async def test_film_search_query(make_get_request):
    query = "war"
    page_size = 20
    response = await make_get_request(method="/film/search", params={"query": query, "page[size]": page_size})
    expected = await expected_data_parser.get_film_data(query=query, page_size=page_size)
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
    expected = await expected_data_parser.get_film_data(query=query, page_size=page_size, genre_id=filter_genre_id)
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
    expected = await expected_data_parser.get_film_data(
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
    expected = await expected_data_parser.get_film_data(
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
    expected = await expected_data_parser.get_film_data(
        query=query, page_size=page_size, page_number=page_number, genre_id=filter_genre_id, sort_by=sort
    )
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_person_search(make_get_request):
    response = await make_get_request(method="/person/search", params={"query": "ford"})
    assert response.status == http.HTTPStatus.OK
    expected = [
        {
            "uuid": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1",
            "full_name": "Harrison Ford",
            "films": [
                {"025c58cd-1b7e-43be-9ffb-8571a613579b": "actor"},
                {"0312ed51-8833-413f-bff5-0e139c11264a": "actor"},
                {"134989c3-3b20-4ae7-8092-3e8ad2333d59": "actor"},
                {"3b1d0e70-42e5-4c9b-98cf-2681c420a99b": "actor"},
                {"3d825f60-9fff-4dfe-b294-1a45fa1e115d": "actor"},
                {"4f53452f-a402-4a76-89fd-f034eeb8d657": "actor"},
                {"b6b8a3b7-1c12-45a8-9da7-4b20db8867df": "actor"},
                {"c7bd11a4-30bf-4077-a618-97c3e5525427": "actor"},
                {"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394": "actor"},
                {"dbb9b244-483b-4592-9194-4938338419bc": "actor"},
                {"f241a62c-2157-432a-bbeb-9c579c8bc18b": "actor"},
            ],
        }
    ]
    assert len(response.body) == 1
    assert response.body == expected


@pytest.mark.asyncio
async def test_person_search_cached(make_get_request, redis_client):
    response = await make_get_request(method="/person/search", params={"query": "ford"})
    assert response.status == http.HTTPStatus.OK
    data = await redis_client.get("person::query::bool::must::multi_match::query::ford")
    data_json = json.loads(data)
    expected = {
        "result": [
            (
                '{"id":"5b4bf1bc-3397-4e83-9b17-8b10c6544ed1",'
                '"fullname":"Harrison Ford",'
                '"film_ids":['
                '{"id":"025c58cd-1b7e-43be-9ffb-8571a613579b",'
                '"title":"Star Wars: Episode VI - Return of the Jedi",'
                '"imdb_rating":8.3,'
                '"role":"actor"},'
                '{"id":"0312ed51-8833-413f-bff5-0e139c11264a",'
                '"title":"Star Wars: Episode V - The Empire Strikes Back",'
                '"imdb_rating":8.7,'
                '"role":"actor"},'
                '{"id":"134989c3-3b20-4ae7-8092-3e8ad2333d59",'
                '"title":"The Star Wars Holiday Special",'
                '"imdb_rating":2.1,'
                '"role":"actor"},'
                '{"id":"3b1d0e70-42e5-4c9b-98cf-2681c420a99b",'
                "\"title\":\"From 'Star Wars' to 'Jedi': The Making of a Saga\","
                '"imdb_rating":7.7,'
                '"role":"actor"},'
                '{"id":"3d825f60-9fff-4dfe-b294-1a45fa1e115d",'
                '"title":"Star Wars: Episode IV - A New Hope",'
                '"imdb_rating":8.6,'
                '"role":"actor"},'
                '{"id":"4f53452f-a402-4a76-89fd-f034eeb8d657",'
                '"title":"Star Wars: Episode V - The Empire Strikes Back: Deleted Scenes",'
                '"imdb_rating":7.6,'
                '"role":"actor"},'
                '{"id":"b6b8a3b7-1c12-45a8-9da7-4b20db8867df",'
                '"title":"Star Wars",'
                '"imdb_rating":7.8,'
                '"role":"actor"},'
                '{"id":"c7bd11a4-30bf-4077-a618-97c3e5525427",'
                '"title":"The Characters of \'Star Wars\'",'
                '"imdb_rating":6.7,'
                '"role":"actor"},'
                '{"id":"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394",'
                '"title":"Star Wars: Episode VII - The Force Awakens",'
                '"imdb_rating":7.9,'
                '"role":"actor"},'
                '{"id":"dbb9b244-483b-4592-9194-4938338419bc",'
                '"title":"Quentin Tarantino\'s Star Wars",'
                '"imdb_rating":4.8,'
                '"role":"actor"},'
                '{"id":"f241a62c-2157-432a-bbeb-9c579c8bc18b",'
                '"title":"Star Wars: Episode IV: A New Hope - Deleted Scenes",'
                '"imdb_rating":8.4,'
                '"role":"actor"}]}'
            )
        ]
    }
    assert data_json == expected
