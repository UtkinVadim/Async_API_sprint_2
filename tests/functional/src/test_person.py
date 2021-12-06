import json

import pytest


@pytest.mark.asyncio
async def test_all_persons(make_get_request):
    response = await make_get_request(method="/person/search", params={"page[size]": "999"})
    assert response.status == 200, response.body
    assert len(response.body) == 20, response.body
    expected = [
        {
            "uuid": "26e83050-29ef-4163-a99d-b546cac208f8",
            "full_name": "Mark Hamill",
            "films": [
                {"025c58cd-1b7e-43be-9ffb-8571a613579b": "actor"},
                {"0312ed51-8833-413f-bff5-0e139c11264a": "actor"},
                {"12a8279d-d851-4eb9-9d64-d690455277cc": "actor"},
                {"134989c3-3b20-4ae7-8092-3e8ad2333d59": "actor"},
                {"3a28f10a-433e-431c-8e7b-cc3f90af5a41": "actor"},
                {"3b1d0e70-42e5-4c9b-98cf-2681c420a99b": "actor"},
                {"3d825f60-9fff-4dfe-b294-1a45fa1e115d": "actor"},
                {"46f15353-2add-415d-9782-fa9c5b8083d5": "actor"},
                {"943946ed-4a2b-4c71-8e0b-a58a11bd1323": "actor"},
                {"b6b8a3b7-1c12-45a8-9da7-4b20db8867df": "actor"},
                {"c7bd11a4-30bf-4077-a618-97c3e5525427": "actor"},
                {"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394": "actor"},
                {"d4b010a5-2648-4850-b15d-307658020923": "director"},
                {"dbb9b244-483b-4592-9194-4938338419bc": "actor"},
            ],
        },
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
        },
        {
            "uuid": "b5d2b63a-ed1f-4e46-8320-cf52a32be358",
            "full_name": "Carrie Fisher",
            "films": [
                {"025c58cd-1b7e-43be-9ffb-8571a613579b": "actor"},
                {"0312ed51-8833-413f-bff5-0e139c11264a": "actor"},
                {"12a8279d-d851-4eb9-9d64-d690455277cc": "actor"},
                {"134989c3-3b20-4ae7-8092-3e8ad2333d59": "actor"},
                {"3d825f60-9fff-4dfe-b294-1a45fa1e115d": "actor"},
                {"46f15353-2add-415d-9782-fa9c5b8083d5": "actor"},
                {"4f53452f-a402-4a76-89fd-f034eeb8d657": "actor"},
                {"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394": "actor"},
                {"f241a62c-2157-432a-bbeb-9c579c8bc18b": "actor"},
            ],
        },
        {
            "uuid": "e039eedf-4daf-452a-bf92-a0085c68e156",
            "full_name": "Peter Cushing",
            "films": [{"3d825f60-9fff-4dfe-b294-1a45fa1e115d": "actor"}, {"73ecd1e6-6326-405a-b51b-69008f383b72": "actor"}],
        },
        {
            "uuid": "1989ed1e-0c0b-4872-9dfb-f5ed13c764e2",
            "full_name": "Irvin Kershner",
            "films": [
                {"0312ed51-8833-413f-bff5-0e139c11264a": "director"},
                {"4f53452f-a402-4a76-89fd-f034eeb8d657": "director"},
                {"a2ff04cc-eede-43fc-a503-07f037be8cc8": "actor"},
            ],
        },
        {
            "uuid": "ed149438-4d76-45c9-861b-d3ed48ccbf0c",
            "full_name": "Leigh Brackett",
            "films": [
                {"0312ed51-8833-413f-bff5-0e139c11264a": "writer"},
                {"4f53452f-a402-4a76-89fd-f034eeb8d657": "writer"},
                {"64aa7000-698f-4332-b52f-9469e4d44ee1": "writer"},
            ],
        },
        {
            "uuid": "3217bc91-bcfc-44eb-a609-82d228115c50",
            "full_name": "Lawrence Kasdan",
            "films": [
                {"025c58cd-1b7e-43be-9ffb-8571a613579b": "writer"},
                {"0312ed51-8833-413f-bff5-0e139c11264a": "writer"},
                {"4f53452f-a402-4a76-89fd-f034eeb8d657": "writer"},
                {"57beb3fd-b1c9-4f8a-9c06-2da13f95251c": "writer"},
                {"64aa7000-698f-4332-b52f-9469e4d44ee1": "writer"},
                {"835dcbe5-2bbc-40a3-8980-eb5605f0e3bf": "actor"},
                {"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394": "writer"},
            ],
        },
        {
            "uuid": "efdd1787-8871-4aa9-b1d7-f68e55b913ed",
            "full_name": "Billy Dee Williams",
            "films": [
                {"025c58cd-1b7e-43be-9ffb-8571a613579b": "actor"},
                {"0312ed51-8833-413f-bff5-0e139c11264a": "actor"},
                {"49a81ffc-1670-4dcd-bbec-e224064cf99c": "actor"},
                {"7dc44185-c268-476d-8b0e-488a091c1d4b": "actor"},
            ],
        },
        {
            "uuid": "3214cf58-8dbf-40ab-9185-77213933507e",
            "full_name": "Richard Marquand",
            "films": [{"025c58cd-1b7e-43be-9ffb-8571a613579b": "director"}],
        },
        {
            "uuid": "a1758395-9578-41af-88b8-3f9456e6d938",
            "full_name": "J.J. Abrams",
            "films": [
                {"075587eb-91c1-4629-adcb-67c516cdb6eb": "actor"},
                {"1d42ceae-9397-475c-9517-e94dda7bc2a1": "actor"},
                {"1dcfed00-a0a1-4042-9811-66d7eb5d94bb": "actor"},
                {"24ef3514-6def-46ff-bf8e-c9bb91aafdfd": "actor"},
                {"46f15353-2add-415d-9782-fa9c5b8083d5": "director"},
                {"49908121-c711-44ee-b447-84288b3b5e34": "actor"},
                {"4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f": "director"},
                {"4e9f5f72-aa45-4c5a-965b-fc9cf42c4299": "actor"},
                {"6ecc7a32-14a1-4da8-9881-bf81f0f09897": "director"},
                {"86607a8f-bc90-47fa-8261-15647186cbf5": "actor"},
                {"a99bbda2-d244-4b38-b32c-761248fb0bf2": "actor"},
                {"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394": "director"},
                {"eb592ca7-7aa8-44ac-a59b-1ffcd0b78960": "actor"},
            ],
        },
        {
            "uuid": "cec00f0e-200b-4b48-9ed1-2f8fc3c67427",
            "full_name": "Michael Arndt",
            "films": [{"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394": "writer"}],
        },
        {
            "uuid": "2d6f6284-13ce-4d25-9453-c4335432c116",
            "full_name": "Adam Driver",
            "films": [
                {"12a8279d-d851-4eb9-9d64-d690455277cc": "actor"},
                {"1d42ceae-9397-475c-9517-e94dda7bc2a1": "actor"},
                {"46f15353-2add-415d-9782-fa9c5b8083d5": "actor"},
                {"91f02795-7628-4ef4-acf2-d93b892365dd": "actor"},
                {"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394": "actor"},
            ],
        },
        {
            "uuid": "979996d5-ef97-427d-a0f5-d640cd1813a4",
            "full_name": "Jake Lloyd",
            "films": [
                {"08a588bd-5eeb-4cf3-8a42-f20195a02c25": "actor"},
                {"17f634cd-9581-4ba1-b40b-89ee058c3f55": "actor"},
                {"3b914679-1f5e-4cbd-8044-d13d35d5236c": "actor"},
                {"569e23df-7e00-459d-b92a-6cb4653d36b8": "actor"},
                {"7a87274a-541a-405c-b148-5946f6c707d4": "actor"},
                {"c5653bd8-56b5-4530-90b2-34ce1a2ba6db": "actor"},
                {"ec8bad1c-7643-49b3-93b5-cee9c8c1e602": "actor"},
            ],
        },
        {
            "uuid": "39abe5bd-33b3-44e8-8c12-2e360e2fa621",
            "full_name": "Liam Neeson",
            "films": [{"3b914679-1f5e-4cbd-8044-d13d35d5236c": "actor"}],
        },
        {
            "uuid": "69b02c62-a329-414d-83c6-ca54be34de24",
            "full_name": "Ewan McGregor",
            "films": [
                {"3b914679-1f5e-4cbd-8044-d13d35d5236c": "actor"},
                {"516f91da-bd70-4351-ba6d-25e16b7713b7": "actor"},
                {"943946ed-4a2b-4c71-8e0b-a58a11bd1323": "actor"},
                {"c4c5e3de-c0c9-4091-b242-ceb331004dfd": "actor"},
            ],
        },
        {
            "uuid": "c777f646-dae0-466f-867a-bc535a0b021b",
            "full_name": "Natalie Portman",
            "films": [
                {"3b914679-1f5e-4cbd-8044-d13d35d5236c": "actor"},
                {"516f91da-bd70-4351-ba6d-25e16b7713b7": "actor"},
                {"c4c5e3de-c0c9-4091-b242-ceb331004dfd": "actor"},
            ],
        },
        {
            "uuid": "62df10e8-244d-4c31-b396-564dfbc2f9c5",
            "full_name": "Hayden Christensen",
            "films": [
                {"516f91da-bd70-4351-ba6d-25e16b7713b7": "actor"},
                {"c4c5e3de-c0c9-4091-b242-ceb331004dfd": "actor"},
                {"daae47e4-cbd0-4ffd-a150-55201b357d5b": "actor"},
            ],
        },
        {
            "uuid": "7214e401-bb43-4da2-9e7a-cd6ca31ee8ca",
            "full_name": "Ian McDiarmid",
            "films": [{"516f91da-bd70-4351-ba6d-25e16b7713b7": "actor"}, {"a20566a2-b3ec-4814-ae9a-040aabcb38e7": "actor"}],
        },
        {
            "uuid": "8c220eeb-8022-44d5-8435-1f8edf258ac7",
            "full_name": "Jonathan Hales",
            "films": [{"c4c5e3de-c0c9-4091-b242-ceb331004dfd": "writer"}],
        },
        {
            "uuid": "ef1e2ad4-df4f-4fe0-8fa9-b8db690c4a19",
            "full_name": "Christopher Lee",
            "films": [{"c4c5e3de-c0c9-4091-b242-ceb331004dfd": "actor"}],
        },
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
    response = await make_get_request(method="/person/5b4bf1bc-3397-4e83-9b17-8b10c6544ed1")
    assert response.status == 200, response.body
    expected = {
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
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_person_films(make_get_request):
    response = await make_get_request(method="/person/5b4bf1bc-3397-4e83-9b17-8b10c6544ed1/film")
    assert response.status == 200, response.body
    assert len(response.body) == 11
    expected = [
        {
            "imdb_rating": 8.3,
            "title": "Star Wars: Episode VI - Return of the Jedi",
            "uuid": "025c58cd-1b7e-43be-9ffb-8571a613579b",
        },
        {
            "imdb_rating": 8.7,
            "title": "Star Wars: Episode V - The Empire Strikes Back",
            "uuid": "0312ed51-8833-413f-bff5-0e139c11264a",
        },
        {"imdb_rating": 2.1, "title": "The Star Wars Holiday Special", "uuid": "134989c3-3b20-4ae7-8092-3e8ad2333d59"},
        {
            "imdb_rating": 7.7,
            "title": "From 'Star Wars' to 'Jedi': The Making of a Saga",
            "uuid": "3b1d0e70-42e5-4c9b-98cf-2681c420a99b",
        },
        {"imdb_rating": 8.6, "title": "Star Wars: Episode IV - A New Hope", "uuid": "3d825f60-9fff-4dfe-b294-1a45fa1e115d"},
        {
            "imdb_rating": 7.6,
            "title": "Star Wars: Episode V - The Empire Strikes Back: Deleted Scenes",
            "uuid": "4f53452f-a402-4a76-89fd-f034eeb8d657",
        },
        {"imdb_rating": 7.8, "title": "Star Wars", "uuid": "b6b8a3b7-1c12-45a8-9da7-4b20db8867df"},
        {"imdb_rating": 6.7, "title": "The Characters of 'Star Wars'", "uuid": "c7bd11a4-30bf-4077-a618-97c3e5525427"},
        {
            "imdb_rating": 7.9,
            "title": "Star Wars: Episode VII - The Force Awakens",
            "uuid": "cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394",
        },
        {"imdb_rating": 4.8, "title": "Quentin Tarantino's Star Wars", "uuid": "dbb9b244-483b-4592-9194-4938338419bc"},
        {
            "imdb_rating": 8.4,
            "title": "Star Wars: Episode IV: A New Hope - Deleted Scenes",
            "uuid": "f241a62c-2157-432a-bbeb-9c579c8bc18b",
        },
    ]
    assert response.body == expected


@pytest.mark.asyncio
async def test_find_person_from_redis_cache(make_get_request, redis_client):
    personfilms = [
        {"id": "1", "title": "Хоббит: Нежданное путешествие", "imdb_rating": 9, "role": "Хоббит"},
        {"id": "2", "title": "Хоббит: Пустошь Смауга", "imdb_rating": 8, "role": "Хоббит"},
        {"id": "3", "title": "Хоббит: Битва пяти воинств", "imdb_rating": 10, "role": "Хоббит"},
    ]
    person = json.dumps({"id": "hobbit_id", "fullname": "Bilbo Baggins", "film_ids": personfilms})
    await redis_client.set("person::hobbit_id", person)
    response = await make_get_request(method="/person/hobbit_id")

    assert response.status == 200

    expected = {"uuid": "hobbit_id", "full_name": "Bilbo Baggins", "films": [{"1": "Хоббит"}, {"2": "Хоббит"}, {"3": "Хоббит"}]}

    assert response.body == expected


@pytest.mark.asyncio
async def test_person_not_found_in_elastic(make_get_request):
    response = await make_get_request(method="/person/good_modern_russian_actor")
    assert response.status == 404, response.body
    expected = {"detail": {"_index": "person", "_type": "_doc", "_id": "good_modern_russian_actor", "found": False}}
    assert response.body == expected
