import pytest


@pytest.mark.asyncio
async def test_all_genres(make_get_request):
    response = await make_get_request(method='/genre/')
    assert response.status == 200, response.body
    assert len(response.body) == 3, response.body
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
            'uuid': '3',
            'name': 'AbraCadabra'
        }
    ]
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_specific_genre(make_get_request, es_client):
    response = await make_get_request(method='/genre/1')

    assert response.status == 200

    expected = {
            'uuid': '1',
            'name': 'Action'
        }

    assert response.body == expected
