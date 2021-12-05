import http
import json

import pytest

expected_films = [
    {'id': '516f91da-bd70-4351-ba6d-25e16b7713b7', 'title': 'Star Wars: Episode III - Revenge of the Sith',
     'imdb_rating': 7.5},
    {'id': 'b1f1e8a6-e310-47d9-a93c-6a7b192bac0e', 'title': 'Star Trek Beyond', 'imdb_rating': 7.1},
    {'id': '6ecc7a32-14a1-4da8-9881-bf81f0f09897', 'title': 'Star Trek Into Darkness', 'imdb_rating': 7.7},
    {'id': '57beb3fd-b1c9-4f8a-9c06-2da13f95251c', 'title': 'Solo: A Star Wars Story', 'imdb_rating': 6.9},
    {'id': '118fd71b-93cd-4de5-95a4-e1485edad30e', 'title': 'Rogue One: A Star Wars Story', 'imdb_rating': 7.8},
    {'id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d', 'title': 'Star Wars: Episode IV - A New Hope',
     'imdb_rating': 8.6},
    {'id': '025c58cd-1b7e-43be-9ffb-8571a613579b', 'title': 'Star Wars: Episode VI - Return of the Jedi',
     'imdb_rating': 8.3},
    {'id': 'cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394', 'title': 'Star Wars: Episode VII - The Force Awakens',
     'imdb_rating': 7.9},
    {'id': '3b914679-1f5e-4cbd-8044-d13d35d5236c', 'title': 'Star Wars: Episode I - The Phantom Menace',
     'imdb_rating': 6.5},
    {'id': 'c4c5e3de-c0c9-4091-b242-ceb331004dfd', 'title': 'Star Wars: Episode II - Attack of the Clones',
     'imdb_rating': 6.5}]

expected_person = [{'uuid': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'full_name': 'Harrison Ford',
                    'films': [{'025c58cd-1b7e-43be-9ffb-8571a613579b': 'actor'},
                              {'0312ed51-8833-413f-bff5-0e139c11264a': 'actor'},
                              {'134989c3-3b20-4ae7-8092-3e8ad2333d59': 'actor'},
                              {'3b1d0e70-42e5-4c9b-98cf-2681c420a99b': 'actor'},
                              {'3d825f60-9fff-4dfe-b294-1a45fa1e115d': 'actor'},
                              {'4f53452f-a402-4a76-89fd-f034eeb8d657': 'actor'},
                              {'b6b8a3b7-1c12-45a8-9da7-4b20db8867df': 'actor'},
                              {'c7bd11a4-30bf-4077-a618-97c3e5525427': 'actor'},
                              {'cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394': 'actor'},
                              {'dbb9b244-483b-4592-9194-4938338419bc': 'actor'},
                              {'f241a62c-2157-432a-bbeb-9c579c8bc18b': 'actor'}]}]

expected_films_genre_filter = [
    {'id': 'b1384a92-f7fe-476b-b90b-6cec2b7a0dce', 'title': 'Star Trek: The Next Generation', 'imdb_rating': 8.6},
    {'id': '4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f', 'title': 'Star Trek', 'imdb_rating': 7.9},
    {'id': 'a7b11817-205f-4e1a-98b5-e3c48b824bc3', 'title': 'Star Trek', 'imdb_rating': 6.4},
    {'id': '6ecc7a32-14a1-4da8-9881-bf81f0f09897', 'title': 'Star Trek Into Darkness', 'imdb_rating': 7.7},
    {'id': 'b1f1e8a6-e310-47d9-a93c-6a7b192bac0e', 'title': 'Star Trek Beyond', 'imdb_rating': 7.1},
    {'id': 'c9e1f6f0-4f1e-4a76-92ee-76c1942faa97', 'title': 'Star Trek: Discovery', 'imdb_rating': 7.3},
    {'id': '50fb4de9-e4b3-4aca-9f2f-00a48f12f9b3', 'title': 'Star Trek: First Contact', 'imdb_rating': 7.6},
    {'id': '6e5cd268-8ce4-45f9-87d2-52f0f26edc9e', 'title': 'Star Trek II: The Wrath of Khan', 'imdb_rating': 7.7}]

expected_films_genre_filter_on_page = [
    {'id': '50fb4de9-e4b3-4aca-9f2f-00a48f12f9b3', 'title': 'Star Trek: First Contact', 'imdb_rating': 7.6},
    {'id': '6ecc7a32-14a1-4da8-9881-bf81f0f09897', 'title': 'Star Trek Into Darkness', 'imdb_rating': 7.7}]

expected_person_cache = {'result': [
    '{"id":"5b4bf1bc-3397-4e83-9b17-8b10c6544ed1","fullname":"Harrison Ford","film_ids":[{"id":"025c58cd-1b7e-43be-9ffb-8571a613579b","title":"Star Wars: Episode VI - Return of the Jedi","imdb_rating":8.3,"role":"actor"},{"id":"0312ed51-8833-413f-bff5-0e139c11264a","title":"Star Wars: Episode V - The Empire Strikes Back","imdb_rating":8.7,"role":"actor"},{"id":"134989c3-3b20-4ae7-8092-3e8ad2333d59","title":"The Star Wars Holiday Special","imdb_rating":2.1,"role":"actor"},{"id":"3b1d0e70-42e5-4c9b-98cf-2681c420a99b","title":"From \'Star Wars\' to \'Jedi\': The Making of a Saga","imdb_rating":7.7,"role":"actor"},{"id":"3d825f60-9fff-4dfe-b294-1a45fa1e115d","title":"Star Wars: Episode IV - A New Hope","imdb_rating":8.6,"role":"actor"},{"id":"4f53452f-a402-4a76-89fd-f034eeb8d657","title":"Star Wars: Episode V - The Empire Strikes Back: Deleted Scenes","imdb_rating":7.6,"role":"actor"},{"id":"b6b8a3b7-1c12-45a8-9da7-4b20db8867df","title":"Star Wars","imdb_rating":7.8,"role":"actor"},{"id":"c7bd11a4-30bf-4077-a618-97c3e5525427","title":"The Characters of \'Star Wars\'","imdb_rating":6.7,"role":"actor"},{"id":"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394","title":"Star Wars: Episode VII - The Force Awakens","imdb_rating":7.9,"role":"actor"},{"id":"dbb9b244-483b-4592-9194-4938338419bc","title":"Quentin Tarantino\'s Star Wars","imdb_rating":4.8,"role":"actor"},{"id":"f241a62c-2157-432a-bbeb-9c579c8bc18b","title":"Star Wars: Episode IV: A New Hope - Deleted Scenes","imdb_rating":8.4,"role":"actor"}]}']}


@pytest.mark.asyncio
async def test_film_search_query(make_get_request, es_client):
    response = await make_get_request(method='/film/search', params={'query': 'war'})
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected_films)
    assert response.body == expected_films


@pytest.mark.asyncio
async def test_film_search_filter(make_get_request, es_client):
    response = await make_get_request(method='/film/search',
                                      params={'query': 'trek', "id": "ca88141b-a6b4-450d-bbc3-efa940e4953f",
                                              'page[size]': '20',
                                              })
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected_films_genre_filter)
    assert response.body == expected_films_genre_filter


@pytest.mark.asyncio
async def test_film_search_sorted_desc(make_get_request, es_client):
    response = await make_get_request(method='/film/search',
                                      params={'query': 'trek', "id": "ca88141b-a6b4-450d-bbc3-efa940e4953f",
                                              'page[size]': '20',
                                              'sort': '-imdb_rating'})
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected_films_genre_filter)
    assert response.body == sorted(expected_films_genre_filter, key=lambda x: x['imdb_rating'], reverse=True)


@pytest.mark.asyncio
async def test_film_search_sorted_asc(make_get_request, es_client):
    response = await make_get_request(method='/film/search',
                                      params={'query': 'trek', "id": "ca88141b-a6b4-450d-bbc3-efa940e4953f",
                                              'page[size]': '20',
                                              'sort': 'imdb_rating'})
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected_films_genre_filter)
    assert response.body == sorted(expected_films_genre_filter, key=lambda x: x['imdb_rating'], reverse=False)


@pytest.mark.asyncio
async def test_film_search_paginator(make_get_request, es_client):
    response = await make_get_request(method='/film/search',
                                      params={'query': 'trek', "id": "ca88141b-a6b4-450d-bbc3-efa940e4953f",
                                              'page[size]': '2', 'page[number]': '3',
                                              'sort': 'imdb_rating'})
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected_films_genre_filter_on_page)
    assert response.body == sorted(expected_films_genre_filter_on_page, key=lambda x: x['imdb_rating'], reverse=False)


@pytest.mark.asyncio
async def test_person_search(make_get_request, es_client):
    response = await make_get_request(method='/person/search', params={'query': 'ford'})
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == len(expected_person)
    assert response.body == expected_person


@pytest.mark.asyncio
async def test_person_search_cached(make_get_request, es_client, redis_client):
    response = await make_get_request(method='/person/search', params={'query': 'ford'})
    assert response.status == http.HTTPStatus.OK
    data = await redis_client.get('person::query::bool::must::multi_match::query::ford')
    data_json = json.loads(data)
    assert data_json == expected_person_cache
