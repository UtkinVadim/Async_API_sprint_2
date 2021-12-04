import pytest


@pytest.mark.asyncio
async def test_search_detailed(make_get_request, es_client):
    await es_client.bulk(
        body=[
            {"index": {"_index": "genre", "_id": "1"}},
            {"id": "1", "name": "Action"},
            {"index": {"_index": "genre", "_id": "2"}},
            {"id": "2", "name": "Comedy"},
            {"index": {"_index": "genre", "_id": "3"}},
            {"id": "3", "name": "AbraCadabra"}
        ],
    )

    response = await make_get_request(method='/genre/')
    print(response.body)

    assert response.status == 200
    assert len(response.body) == 3

    expected = [
        {
            'uuid': '1',
            'name': 'Action'
        },
        {
            'uuid': '2',
            'name': 'Comedy'
        },
        {
            'uuid': '3', 'name': 'AbraCadabra'
        }
    ]

    assert response.body == expected
