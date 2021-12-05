import json

import pytest

expected = [{'name': 'Action', 'uuid': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff'},
            {'name': 'Adventure', 'uuid': '120a21cf-9097-479e-904a-13dd7198c1dd'},
            {'name': 'Fantasy', 'uuid': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd'},
            {'name': 'Sci-Fi', 'uuid': '6c162475-c7ed-4461-9184-001ef3d9f26e'},
            {'name': 'Drama', 'uuid': '1cacff68-643e-4ddd-8f57-84b62538081a'},
            {'name': 'Music', 'uuid': '56b541ab-4d66-4021-8708-397762bff2d4'},
            {'name': 'Romance', 'uuid': '237fd1e4-c98e-454e-aa13-8a13fb7547b5'},
            {'name': 'Thriller', 'uuid': '526769d7-df18-4661-9aa6-49ed24e9dfd8'},
            {'name': 'Mystery', 'uuid': 'ca88141b-a6b4-450d-bbc3-efa940e4953f'},
            {'name': 'Animation', 'uuid': '6a0a479b-cfec-41ac-b520-41b2b007b611'},
            {'name': 'Family', 'uuid': '55c723c1-6d90-4a04-a44b-e9792040251a'},
            {'name': 'Biography', 'uuid': 'ca124c76-9760-4406-bfa0-409b1e38d200'},
            {'name': 'Musical', 'uuid': '9c91a5b2-eb70-4889-8581-ebe427370edd'},
            {'name': 'Crime', 'uuid': '63c24835-34d3-4279-8d81-3c5f4ddb0cdc'},
            {'name': 'Short', 'uuid': 'a886d0ec-c3f3-4b16-b973-dedcf5bfa395'},
            {'name': 'Western', 'uuid': '0b105f87-e0a5-45dc-8ce7-f8632088f390'},
            {'name': 'Documentary', 'uuid': '6d141ad2-d407-4252-bda4-95590aaf062a'},
            {'name': 'History', 'uuid': 'eb7212a7-dd10-4552-bf7b-7a505a8c0b95'},
            {'name': 'War', 'uuid': 'c020dab2-e9bd-4758-95ca-dbe363462173'},
            {'name': 'Reality-TV', 'uuid': 'e508c1c8-24c0-4136-80b4-340c4befb190'}]

expected_cache = {'result': ['{"id":"3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff","name":"Action"}',
                             '{"id":"120a21cf-9097-479e-904a-13dd7198c1dd","name":"Adventure"}',
                             '{"id":"b92ef010-5e4c-4fd0-99d6-41b6456272cd","name":"Fantasy"}',
                             '{"id":"6c162475-c7ed-4461-9184-001ef3d9f26e","name":"Sci-Fi"}',
                             '{"id":"1cacff68-643e-4ddd-8f57-84b62538081a","name":"Drama"}',
                             '{"id":"56b541ab-4d66-4021-8708-397762bff2d4","name":"Music"}',
                             '{"id":"237fd1e4-c98e-454e-aa13-8a13fb7547b5","name":"Romance"}',
                             '{"id":"526769d7-df18-4661-9aa6-49ed24e9dfd8","name":"Thriller"}',
                             '{"id":"ca88141b-a6b4-450d-bbc3-efa940e4953f","name":"Mystery"}',
                             '{"id":"6a0a479b-cfec-41ac-b520-41b2b007b611","name":"Animation"}',
                             '{"id":"55c723c1-6d90-4a04-a44b-e9792040251a","name":"Family"}',
                             '{"id":"ca124c76-9760-4406-bfa0-409b1e38d200","name":"Biography"}',
                             '{"id":"9c91a5b2-eb70-4889-8581-ebe427370edd","name":"Musical"}',
                             '{"id":"63c24835-34d3-4279-8d81-3c5f4ddb0cdc","name":"Crime"}',
                             '{"id":"a886d0ec-c3f3-4b16-b973-dedcf5bfa395","name":"Short"}',
                             '{"id":"0b105f87-e0a5-45dc-8ce7-f8632088f390","name":"Western"}',
                             '{"id":"6d141ad2-d407-4252-bda4-95590aaf062a","name":"Documentary"}',
                             '{"id":"eb7212a7-dd10-4552-bf7b-7a505a8c0b95","name":"History"}',
                             '{"id":"c020dab2-e9bd-4758-95ca-dbe363462173","name":"War"}',
                             '{"id":"e508c1c8-24c0-4136-80b4-340c4befb190","name":"Reality-TV"}']}


@pytest.mark.asyncio
async def test_search_detailed(make_get_request, es_client):
    response = await make_get_request(method='/genre/')

    print(response.status)

    assert response.status == 200
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
async def test_cache_search_detailed(make_get_request, es_client, redis_client):
    response = await make_get_request(method='/genre/')
    assert response.status == 200
    data = await redis_client.get('genre::size::999')

    data_json = json.loads(data)
    assert data_json == expected_cache


