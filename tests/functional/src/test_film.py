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
    response = await make_get_request(
        method="/film", params={"page[size]": page_size}
    )
    assert response.status == http.HTTPStatus.OK
    expected = await expected_data_parser.get_film_data(page_size=page_size)
    assert len(response.body) == page_size
    assert response.body == expected


@pytest.mark.asyncio
async def test_film_filter_sorted_desc(make_get_request):
    page_size = 5
    sort = "-imdb_rating"
    response = await make_get_request(
        method="/film", params={"page[size]": page_size, "sort": sort}
    )
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
    response = await make_get_request(
        method="/film",
        params={"id": "ca88141b-a6b4-450d-bbc3-efa940e4953f", "page[size]": "2", "page[number]": "3", "sort": "imdb_rating"},
    )
    assert response.status == http.HTTPStatus.OK
    expected = [
        {
            "id": "46f15353-2add-415d-9782-fa9c5b8083d5",
            "title": "Star Wars: Episode IX - The Rise of Skywalker",
            "imdb_rating": 6.7,
        },
        {"id": "57beb3fd-b1c9-4f8a-9c06-2da13f95251c", "title": "Solo: A Star Wars Story", "imdb_rating": 6.9},
    ]
    assert len(response.body) == 2
    assert response.body == expected


expected_films_all = [
    {"id": "3d825f60-9fff-4dfe-b294-1a45fa1e115d", "title": "Star Wars: Episode IV - A New Hope", "imdb_rating": 8.6},
    {"id": "0312ed51-8833-413f-bff5-0e139c11264a", "title": "Star Wars: Episode V - The Empire Strikes Back", "imdb_rating": 8.7},
    {"id": "025c58cd-1b7e-43be-9ffb-8571a613579b", "title": "Star Wars: Episode VI - Return of the Jedi", "imdb_rating": 8.3},
    {"id": "cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394", "title": "Star Wars: Episode VII - The Force Awakens", "imdb_rating": 7.9},
    {"id": "3b914679-1f5e-4cbd-8044-d13d35d5236c", "title": "Star Wars: Episode I - The Phantom Menace", "imdb_rating": 6.5},
    {"id": "516f91da-bd70-4351-ba6d-25e16b7713b7", "title": "Star Wars: Episode III - Revenge of the Sith", "imdb_rating": 7.5},
    {"id": "c4c5e3de-c0c9-4091-b242-ceb331004dfd", "title": "Star Wars: Episode II - Attack of the Clones", "imdb_rating": 6.5},
    {"id": "4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f", "title": "Star Trek", "imdb_rating": 7.9},
    {"id": "12a8279d-d851-4eb9-9d64-d690455277cc", "title": "Star Wars: Episode VIII - The Last Jedi", "imdb_rating": 7.0},
    {"id": "118fd71b-93cd-4de5-95a4-e1485edad30e", "title": "Rogue One: A Star Wars Story", "imdb_rating": 7.8},
    {"id": "6ecc7a32-14a1-4da8-9881-bf81f0f09897", "title": "Star Trek Into Darkness", "imdb_rating": 7.7},
    {"id": "46f15353-2add-415d-9782-fa9c5b8083d5", "title": "Star Wars: Episode IX - The Rise of Skywalker", "imdb_rating": 6.7},
    {"id": "fda827f8-d261-4c23-9e9c-e42787580c4d", "title": "A Star Is Born", "imdb_rating": 7.7},
    {"id": "57beb3fd-b1c9-4f8a-9c06-2da13f95251c", "title": "Solo: A Star Wars Story", "imdb_rating": 6.9},
    {"id": "b1f1e8a6-e310-47d9-a93c-6a7b192bac0e", "title": "Star Trek Beyond", "imdb_rating": 7.1},
    {"id": "50fb4de9-e4b3-4aca-9f2f-00a48f12f9b3", "title": "Star Trek: First Contact", "imdb_rating": 7.6},
    {"id": "6e5cd268-8ce4-45f9-87d2-52f0f26edc9e", "title": "Star Trek II: The Wrath of Khan", "imdb_rating": 7.7},
    {"id": "b1384a92-f7fe-476b-b90b-6cec2b7a0dce", "title": "Star Trek: The Next Generation", "imdb_rating": 8.6},
    {"id": "c9e1f6f0-4f1e-4a76-92ee-76c1942faa97", "title": "Star Trek: Discovery", "imdb_rating": 7.3},
    {"id": "a7b11817-205f-4e1a-98b5-e3c48b824bc3", "title": "Star Trek", "imdb_rating": 6.4},
]


@pytest.mark.asyncio
async def test_film_filter_all(make_get_request):
    response = await make_get_request(method="/film", params={"page[size]": "9999"})
    assert response.status == http.HTTPStatus.OK

    assert len(response.body) == 20
    assert response.body == expected_films_all


@pytest.mark.asyncio
async def test_film_filter_all_cached(make_get_request, redis_client):
    response = await make_get_request(method="/film", params={"page[size]": "9999"})
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == 20
    assert response.body == expected_films_all
    data = await redis_client.get("movies::query::bool::must::match_all::size::9999")
    data_json = json.loads(data)
    expected = {
        "result": [
            '{"id":"3d825f60-9fff-4dfe-b294-1a45fa1e115d","title":"Star Wars: Episode IV - A New Hope","imdb_rating":8.6,"description":"The Imperial Forces, under orders from cruel Darth Vader, hold Princess Leia hostage in their efforts to quell the rebellion against the Galactic Empire. Luke Skywalker and Han Solo, captain of the Millennium Falcon, work together with the companionable droid duo R2-D2 and C-3PO to rescue the beautiful princess, help the Rebel Alliance and restore freedom and justice to the Galaxy.","genre":["Fantasy","Adventure","Sci-Fi","Action"],"director":null,"actors":[{"id":"b5d2b63a-ed1f-4e46-8320-cf52a32be358","name":"Carrie Fisher"},{"id":"5b4bf1bc-3397-4e83-9b17-8b10c6544ed1","name":"Harrison Ford"},{"id":"26e83050-29ef-4163-a99d-b546cac208f8","name":"Mark Hamill"},{"id":"e039eedf-4daf-452a-bf92-a0085c68e156","name":"Peter Cushing"}],"writers":[{"id":"a5a8f573-3cee-4ccc-8a2b-91cb9f55250a","name":"George Lucas"}]}',
            '{"id":"0312ed51-8833-413f-bff5-0e139c11264a","title":"Star Wars: Episode V - The Empire Strikes Back","imdb_rating":8.7,"description":"Luke Skywalker, Han Solo, Princess Leia and Chewbacca face attack by the Imperial forces and its AT-AT walkers on the ice planet Hoth. While Han and Leia escape in the Millennium Falcon, Luke travels to Dagobah in search of Yoda. Only with the Jedi master\'s help will Luke survive when the dark side of the Force beckons him into the ultimate duel with Darth Vader.","genre":["Adventure","Sci-Fi","Fantasy","Action"],"director":"Irvin Kershner","actors":[{"id":"efdd1787-8871-4aa9-b1d7-f68e55b913ed","name":"Billy Dee Williams"},{"id":"5b4bf1bc-3397-4e83-9b17-8b10c6544ed1","name":"Harrison Ford"},{"id":"b5d2b63a-ed1f-4e46-8320-cf52a32be358","name":"Carrie Fisher"},{"id":"26e83050-29ef-4163-a99d-b546cac208f8","name":"Mark Hamill"}],"writers":[{"id":"ed149438-4d76-45c9-861b-d3ed48ccbf0c","name":"Leigh Brackett"},{"id":"3217bc91-bcfc-44eb-a609-82d228115c50","name":"Lawrence Kasdan"},{"id":"a5a8f573-3cee-4ccc-8a2b-91cb9f55250a","name":"George Lucas"}]}',
            '{"id":"025c58cd-1b7e-43be-9ffb-8571a613579b","title":"Star Wars: Episode VI - Return of the Jedi","imdb_rating":8.3,"description":"Luke Skywalker battles horrible Jabba the Hut and cruel Darth Vader to save his comrades in the Rebel Alliance and triumph over the Galactic Empire. Han Solo and Princess Leia reaffirm their love and team with Chewbacca, Lando Calrissian, the Ewoks and the androids C-3PO and R2-D2 to aid in the disruption of the Dark Side and the defeat of the evil emperor.","genre":["Adventure","Sci-Fi","Fantasy","Action"],"director":"Richard Marquand","actors":[{"id":"26e83050-29ef-4163-a99d-b546cac208f8","name":"Mark Hamill"},{"id":"b5d2b63a-ed1f-4e46-8320-cf52a32be358","name":"Carrie Fisher"},{"id":"5b4bf1bc-3397-4e83-9b17-8b10c6544ed1","name":"Harrison Ford"},{"id":"efdd1787-8871-4aa9-b1d7-f68e55b913ed","name":"Billy Dee Williams"}],"writers":[{"id":"3217bc91-bcfc-44eb-a609-82d228115c50","name":"Lawrence Kasdan"},{"id":"a5a8f573-3cee-4ccc-8a2b-91cb9f55250a","name":"George Lucas"}]}',
            '{"id":"cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394","title":"Star Wars: Episode VII - The Force Awakens","imdb_rating":7.9,"description":"30 years after the defeat of Darth Vader and the Empire, Rey, a scavenger from the planet Jakku, finds a BB-8 droid that knows the whereabouts of the long lost Luke Skywalker. Rey, as well as a rogue stormtrooper and two smugglers, are thrown into the middle of a battle between the Resistance and the daunting legions of the First Order.","genre":["Adventure","Action","Sci-Fi"],"director":"J.J. Abrams","actors":[{"id":"26e83050-29ef-4163-a99d-b546cac208f8","name":"Mark Hamill"},{"id":"b5d2b63a-ed1f-4e46-8320-cf52a32be358","name":"Carrie Fisher"},{"id":"5b4bf1bc-3397-4e83-9b17-8b10c6544ed1","name":"Harrison Ford"},{"id":"2d6f6284-13ce-4d25-9453-c4335432c116","name":"Adam Driver"}],"writers":[{"id":"a5a8f573-3cee-4ccc-8a2b-91cb9f55250a","name":"George Lucas"},{"id":"cec00f0e-200b-4b48-9ed1-2f8fc3c67427","name":"Michael Arndt"},{"id":"3217bc91-bcfc-44eb-a609-82d228115c50","name":"Lawrence Kasdan"}]}',
            '{"id":"3b914679-1f5e-4cbd-8044-d13d35d5236c","title":"Star Wars: Episode I - The Phantom Menace","imdb_rating":6.5,"description":"The evil Trade Federation, led by Nute Gunray is planning to take over the peaceful world of Naboo. Jedi Knights Qui-Gon Jinn and Obi-Wan Kenobi are sent to confront the leaders. But not everything goes to plan. The two Jedi escape, and along with their new Gungan friend, Jar Jar Binks head to Naboo to warn Queen Amidala, but droids have already started to capture Naboo and the Queen is not safe there. Eventually, they land on Tatooine, where they become friends with a young boy known as Anakin Skywalker. Qui-Gon is curious about the boy, and sees a bright future for him. The group must now find a way of getting to Coruscant and to finally solve this trade dispute, but there is someone else hiding in the shadows. Are the Sith really extinct? Is the Queen really who she says she is? And what\'s so special about this young boy?","genre":["Action","Fantasy","Adventure","Sci-Fi"],"director":"George Lucas","actors":[{"id":"979996d5-ef97-427d-a0f5-d640cd1813a4","name":"Jake Lloyd"},{"id":"39abe5bd-33b3-44e8-8c12-2e360e2fa621","name":"Liam Neeson"},{"id":"c777f646-dae0-466f-867a-bc535a0b021b","name":"Natalie Portman"},{"id":"69b02c62-a329-414d-83c6-ca54be34de24","name":"Ewan McGregor"}],"writers":null}',
            '{"id":"516f91da-bd70-4351-ba6d-25e16b7713b7","title":"Star Wars: Episode III - Revenge of the Sith","imdb_rating":7.5,"description":"Near the end of the Clone Wars, Darth Sidious has revealed himself and is ready to execute the last part of his plan to rule the galaxy. Sidious is ready for his new apprentice, Darth Vader, to step into action and kill the remaining Jedi. Vader, however, struggles to choose the dark side and save his wife or remain loyal to the Jedi order.","genre":["Action","Adventure","Fantasy","Sci-Fi"],"director":"George Lucas","actors":[{"id":"62df10e8-244d-4c31-b396-564dfbc2f9c5","name":"Hayden Christensen"},{"id":"c777f646-dae0-466f-867a-bc535a0b021b","name":"Natalie Portman"},{"id":"7214e401-bb43-4da2-9e7a-cd6ca31ee8ca","name":"Ian McDiarmid"},{"id":"69b02c62-a329-414d-83c6-ca54be34de24","name":"Ewan McGregor"}],"writers":null}',
            '{"id":"c4c5e3de-c0c9-4091-b242-ceb331004dfd","title":"Star Wars: Episode II - Attack of the Clones","imdb_rating":6.5,"description":"Ten years after the invasion of Naboo, the Galactic Republic is facing a Separatist movement and the former queen and now Senator Padmé Amidala travels to Coruscant to vote on a project to create an army to help the Jedi to protect the Republic. Upon arrival, she escapes from an attempt to kill her, and Obi-Wan Kenobi and his Padawan Anakin Skywalker are assigned to protect her. They chase the shape-shifter Zam Wessell but she is killed by a poisoned dart before revealing who hired her. The Jedi Council assigns Obi-Wan Kenobi to discover who has tried to kill Amidala and Anakin to protect her in Naboo. Obi-Wan discovers that the dart is from the planet Kamino, and he heads to the remote planet. He finds an army of clones that has been under production for years for the Republic and that the bounty hunter Jango Fett was the matrix for the clones. Meanwhile Anakin and Amidala fall in love with each other, and he has nightmarish visions of his mother. They travel to his home planet, Tatooine, to see his mother, and he discovers that she has been abducted by Tusken Raiders. Anakin finds his mother dying, and he kills all the Tusken tribe, including the women and children. Obi-Wan follows Jango Fett to the planet Geonosis where he discovers who is behind the Separatist movement. He transmits his discoveries to Anakin since he cannot reach the Jedi Council. Who is the leader of the Separatist movement? Will Anakin receive Obi-Wan\'s message? And will the secret love between Anakin and Amidala succeed?","genre":["Adventure","Sci-Fi","Action","Fantasy"],"director":"George Lucas","actors":[{"id":"ef1e2ad4-df4f-4fe0-8fa9-b8db690c4a19","name":"Christopher Lee"},{"id":"62df10e8-244d-4c31-b396-564dfbc2f9c5","name":"Hayden Christensen"},{"id":"69b02c62-a329-414d-83c6-ca54be34de24","name":"Ewan McGregor"},{"id":"c777f646-dae0-466f-867a-bc535a0b021b","name":"Natalie Portman"}],"writers":[{"id":"8c220eeb-8022-44d5-8435-1f8edf258ac7","name":"Jonathan Hales"}]}',
            '{"id":"4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f","title":"Star Trek","imdb_rating":7.9,"description":"On the day of James Kirk\'s birth, his father dies on his damaged starship in a last stand against a Romulan mining vessel looking for Ambassador Spock, who in this time, has grown on Vulcan disdained by his neighbors for his half-human heritage. 25 years later, James T. Kirk has grown into a young rebellious troublemaker. Challenged by Captain Christopher Pike to realize his potential in Starfleet, he comes to annoy academy instructors like Commander Spock. Suddenly, there is an emergency on Vulcan and the newly-commissioned USS Enterprise is crewed with promising cadets like Nyota Uhura, Hikaru Sulu, Pavel Chekov and even Kirk himself, thanks to Leonard McCoy\'s medical trickery. Together, this crew will have an adventure in the final frontier where the old legend is altered forever as a new version of the legend begins.","genre":["Sci-Fi","Adventure","Action"],"director":"J.J. Abrams","actors":[{"id":"959d148c-022b-427f-a68b-bbe58674fe65","name":"Eric Bana"},{"id":"9f38323f-5912-40d2-a90c-b56899746f2a","name":"Chris Pine"},{"id":"8a34f121-7ce6-4021-b467-abec993fc6cd","name":"Zachary Quinto"},{"id":"5a3d0299-2df2-4070-9fda-65ff4dfa863c","name":"Leonard Nimoy"}],"writers":[{"id":"9b58c99a-e5a3-4f24-8f67-a038665758d6","name":"Roberto Orci"},{"id":"82b7dffe-6254-4598-b6ef-5be747193946","name":"Alex Kurtzman"},{"id":"6960e2ca-889f-41f5-b728-1e7313e54d6c","name":"Gene Roddenberry"}]}',
            '{"id":"12a8279d-d851-4eb9-9d64-d690455277cc","title":"Star Wars: Episode VIII - The Last Jedi","imdb_rating":7.0,"description":"Rey develops her newly discovered abilities with the guidance of Luke Skywalker, who is unsettled by the strength of her powers. Meanwhile, the Resistance prepares for battle with the First Order.","genre":["Action","Adventure","Sci-Fi","Fantasy"],"director":"Rian Johnson","actors":[{"id":"26e83050-29ef-4163-a99d-b546cac208f8","name":"Mark Hamill"},{"id":"2d6f6284-13ce-4d25-9453-c4335432c116","name":"Adam Driver"},{"id":"b5d2b63a-ed1f-4e46-8320-cf52a32be358","name":"Carrie Fisher"},{"id":"7026c3f4-d7b8-414a-99d5-06de1788a0ee","name":"Daisy Ridley"}],"writers":[{"id":"a5a8f573-3cee-4ccc-8a2b-91cb9f55250a","name":"George Lucas"}]}',
            '{"id":"118fd71b-93cd-4de5-95a4-e1485edad30e","title":"Rogue One: A Star Wars Story","imdb_rating":7.8,"description":"All looks lost for the Rebellion against the Empire as they learn of the existence of a new super weapon, the Death Star. Once a possible weakness in its construction is uncovered, the Rebel Alliance must set out on a desperate mission to steal the plans for the Death Star. The future of the entire galaxy now rests upon its success.","genre":["Action","Sci-Fi","Adventure"],"director":"Gareth Edwards","actors":[{"id":"c59c5caf-5ca9-430e-bde5-f5141de25cb6","name":"Alan Tudyk"},{"id":"ccb3418a-d3e2-4878-a355-6f720211f39f","name":"Felicity Jones"},{"id":"6e2f9652-460b-4c6a-b527-5c05b40965fe","name":"Donnie Yen"},{"id":"ac44d92b-7de3-4274-908f-0173e6ba310b","name":"Diego Luna"}],"writers":[{"id":"e0dd7338-b686-465c-93da-c9b2c57d46bb","name":"Gary Whitta"},{"id":"a5a8f573-3cee-4ccc-8a2b-91cb9f55250a","name":"George Lucas"},{"id":"6d9a226f-85ca-4270-9f26-7d1b1cc7b444","name":"Tony Gilroy"},{"id":"5bd4381f-5763-474f-baa0-f7f62a0819f9","name":"John Knoll"},{"id":"06d3686f-56e0-40df-81ea-af95a203b58a","name":"Chris Weitz"}]}',
            '{"id":"6ecc7a32-14a1-4da8-9881-bf81f0f09897","title":"Star Trek Into Darkness","imdb_rating":7.7,"description":"When the USS Enterprise crew is called back home, they find an unstoppable force of terror from within their own organization has detonated the fleet and everything it stands for, leaving our world in a state of crisis. With a personal score to settle, Captain Kirk leads a manhunt to a war-zone world to capture a one-man weapon of mass destruction. As our space heroes are propelled into an epic chess game of life and death, love will be challenged, friendships will be torn apart, and sacrifices must be made for the only family Kirk has left: his crew.","genre":["Action","Sci-Fi","Adventure"],"director":"J.J. Abrams","actors":[{"id":"afa7c253-6702-47d7-a451-cf2bc9350310","name":"Karl Urban"},{"id":"4a416628-4a36-431c-9121-513674dae840","name":"Zoe Saldana"},{"id":"8a34f121-7ce6-4021-b467-abec993fc6cd","name":"Zachary Quinto"},{"id":"9f38323f-5912-40d2-a90c-b56899746f2a","name":"Chris Pine"}],"writers":[{"id":"dbac6947-e620-4f92-b6a1-dae9a3b07422","name":"Damon Lindelof"},{"id":"82b7dffe-6254-4598-b6ef-5be747193946","name":"Alex Kurtzman"},{"id":"6960e2ca-889f-41f5-b728-1e7313e54d6c","name":"Gene Roddenberry"},{"id":"9b58c99a-e5a3-4f24-8f67-a038665758d6","name":"Roberto Orci"}]}',
            '{"id":"46f15353-2add-415d-9782-fa9c5b8083d5","title":"Star Wars: Episode IX - The Rise of Skywalker","imdb_rating":6.7,"description":"The surviving members of the resistance face the First Order once again, and the legendary conflict between the Jedi and the Sith reaches its peak bringing the Skywalker saga to its end.","genre":["Sci-Fi","Adventure","Action","Fantasy"],"director":"J.J. Abrams","actors":[{"id":"b5d2b63a-ed1f-4e46-8320-cf52a32be358","name":"Carrie Fisher"},{"id":"7026c3f4-d7b8-414a-99d5-06de1788a0ee","name":"Daisy Ridley"},{"id":"26e83050-29ef-4163-a99d-b546cac208f8","name":"Mark Hamill"},{"id":"2d6f6284-13ce-4d25-9453-c4335432c116","name":"Adam Driver"}],"writers":[{"id":"cdf3ace6-802d-4620-b875-809e6318a493","name":"Chris Terrio"},{"id":"26e020b4-98d9-4c78-b85a-0570eb19d9bc","name":"Derek Connolly"},{"id":"5623ae85-91ff-44f1-b46d-21c9d1d0d7f6","name":"Colin Trevorrow"},{"id":"a5a8f573-3cee-4ccc-8a2b-91cb9f55250a","name":"George Lucas"}]}',
            '{"id":"fda827f8-d261-4c23-9e9c-e42787580c4d","title":"A Star Is Born","imdb_rating":7.7,"description":"Jackson Maine (Cooper), a country music star on the brink of decline, discovers a talented unknown named Ally (Germanotta). As the two begin a passionate love affair, Jackson coaxes Ally into the spotlight, catapulting her to stardom. But as Ally\'s career quickly eclipses his own, Jack finds it increasingly hard to handle his fading glory.","genre":["Drama","Music","Romance"],"director":"Bradley Cooper","actors":[{"id":"77789b44-e734-4fa6-91e8-212a09fa4a32","name":"Lady Gaga"},{"id":"e52627f7-a659-476a-b415-e58e6bebe824","name":"Sam Elliott"},{"id":"fe2b0699-b5ac-437a-9a69-e747b11eb641","name":"Andrew Dice Clay"}],"writers":[{"id":"39276c87-27ec-42f3-a573-e0184fc463a7","name":"Eric Roth"},{"id":"dd0d82d8-1c95-4bb9-b9c6-d707773aa4db","name":"Will Fetters"},{"id":"e259d88e-b693-436a-9fed-a10204b8fd91","name":"Robert Carson"},{"id":"f24f3fa4-2e42-4dde-be8c-2aba541a593b","name":"Joan Didion"},{"id":"5ac68e18-a84c-4a98-a2ba-85d1bc85e0a4","name":"William A. Wellman"},{"id":"e31f6518-6f0a-4738-a224-211eb4150e13","name":"Frank Pierson"},{"id":"2b0f84fb-416b-4c30-80db-69478bf872be","name":"John Gregory Dunne"},{"id":"7fb9ae3d-aeac-40a9-aa25-cd6992be16a6","name":"Moss Hart"}]}',
            '{"id":"57beb3fd-b1c9-4f8a-9c06-2da13f95251c","title":"Solo: A Star Wars Story","imdb_rating":6.9,"description":"During an adventure into the criminal underworld, Han Solo meets his future co-pilot Chewbacca and encounters Lando Calrissian years before joining the Rebellion.","genre":["Sci-Fi","Adventure","Action"],"director":"Ron Howard","actors":[{"id":"ce06e6d7-600b-4829-badf-5d02c61f1a92","name":"Alden Ehrenreich"},{"id":"c69da9bd-eb87-4a06-be70-95d4ee2da1cc","name":"Joonas Suotamo"},{"id":"7a852205-2bf6-4b75-b3b2-8a46ed6e91ef","name":"Emilia Clarke"},{"id":"01377f6d-9767-48ce-9e37-3c81f8a3c739","name":"Woody Harrelson"}],"writers":[{"id":"a2c091a2-281e-4732-9357-79b213d8d92f","name":"Jonathan Kasdan"},{"id":"3217bc91-bcfc-44eb-a609-82d228115c50","name":"Lawrence Kasdan"},{"id":"a5a8f573-3cee-4ccc-8a2b-91cb9f55250a","name":"George Lucas"}]}',
            '{"id":"b1f1e8a6-e310-47d9-a93c-6a7b192bac0e","title":"Star Trek Beyond","imdb_rating":7.1,"description":"After stopping off at Starbase Yorktown, a remote outpost on the fringes of Federation space, the USS Enterprise, halfway into their five-year mission, is destroyed by an unstoppable wave of unknown aliens. With the crew stranded on an unknown planet and with no apparent means of rescue, they find themselves fighting against a ruthless enemy with a well-earned hatred of the Federation and everything it stands for. Only a rebellious alien warrior can help them reunite and leave the planet to stop this deadly menace from beginning a possible galactic war.","genre":["Adventure","Sci-Fi","Thriller","Action"],"director":"Justin Lin","actors":[{"id":"9f38323f-5912-40d2-a90c-b56899746f2a","name":"Chris Pine"},{"id":"8a34f121-7ce6-4021-b467-abec993fc6cd","name":"Zachary Quinto"},{"id":"afa7c253-6702-47d7-a451-cf2bc9350310","name":"Karl Urban"},{"id":"4a416628-4a36-431c-9121-513674dae840","name":"Zoe Saldana"}],"writers":[{"id":"2cf03687-ebc3-47dc-a99f-602f6cc55f7a","name":"Simon Pegg"},{"id":"6960e2ca-889f-41f5-b728-1e7313e54d6c","name":"Gene Roddenberry"},{"id":"698522c6-f8e9-403a-8922-9d320dec5753","name":"Doug Jung"}]}',
            '{"id":"50fb4de9-e4b3-4aca-9f2f-00a48f12f9b3","title":"Star Trek: First Contact","imdb_rating":7.6,"description":"In the 24th century, the crew of the Enterprise-E has been ordered to patrol the Romulan Neutral Zone by the Federation to avoid interference with their battle against the insidious Borg. Witnessing the loss of the battle, Captain Jean-Luc Picard ignores orders and takes command of the fleet engaging the Borg. But the Borg plan to travel back into the 21st century through a vortex with the intention to stop Earth\'s first contact with an alien race (the Vulcans). Following the Borg sphere, Picard and his crew realize that they have taken over the Enterprise in order to carry out their mission. Their only chance to do away with the Borg and their seductive queen is to make sure that Zefram Cochrane makes his famous faster-than-light travel to the stars.","genre":["Adventure","Drama","Thriller","Sci-Fi","Action"],"director":null,"actors":[{"id":"972c86a5-16f4-432b-b9b3-54965291ddb0","name":"Brent Spiner"},{"id":"fc9f27d2-aaee-46e6-b263-40ec8d2dd355","name":"LeVar Burton"},{"id":"57a471b1-09dc-48fd-ba8a-1211015a0110","name":"Patrick Stewart"},{"id":"5bddea2c-8609-499a-a444-77e0142743c0","name":"Jonathan Frakes"}],"writers":[{"id":"d67d5cb8-4541-4b20-89be-4100ba95e615","name":"Brannon Braga"},{"id":"382da5d5-135b-4b02-a069-ba9beb5f3786","name":"Ronald D. Moore"},{"id":"6960e2ca-889f-41f5-b728-1e7313e54d6c","name":"Gene Roddenberry"},{"id":"88a99b4d-4d06-4754-b06c-93217cf53244","name":"Rick Berman"}]}',
            '{"id":"6e5cd268-8ce4-45f9-87d2-52f0f26edc9e","title":"Star Trek II: The Wrath of Khan","imdb_rating":7.7,"description":"It is the 23rd century. Admiral James T. Kirk is an instructor at Starfleet Academy and feeling old; the prospect of attending his ship, the USS Enterprise--now a training ship--on a two-week cadet cruise does not make him feel any younger. But the training cruise becomes a deadly serious mission when his nemesis Khan Noonien Singh--infamous conqueror from late 20th century Earth--appears after years of exile. Khan later revealed that the planet Ceti Alpha VI exploded, and shifted the orbit of the fifth planet as a Mars-like haven. He begins capturing Project Genesis, a top secret device holding the power of creation itself, and schemes the utter destruction of Kirk.","genre":["Action","Adventure","Sci-Fi"],"director":"Nicholas Meyer","actors":[{"id":"5a3d0299-2df2-4070-9fda-65ff4dfa863c","name":"Leonard Nimoy"},{"id":"9758b894-57d7-465d-b657-c5803dd5b7f7","name":"William Shatner"},{"id":"807ce9c3-6294-485c-803a-1975066f239f","name":"James Doohan"},{"id":"836bb95b-6db8-4418-a110-f41663b1c025","name":"DeForest Kelley"}],"writers":[{"id":"58411ec0-c40a-43da-95e3-0adc74b7e7f6","name":"Harve Bennett"},{"id":"24b5b1fb-9931-4964-a0d2-ce664c00c1d5","name":"Jack B. Sowards"},{"id":"6960e2ca-889f-41f5-b728-1e7313e54d6c","name":"Gene Roddenberry"}]}',
            '{"id":"b1384a92-f7fe-476b-b90b-6cec2b7a0dce","title":"Star Trek: The Next Generation","imdb_rating":8.6,"description":"Set in the 24th century and decades after the adventures of the original crew of the starship Enterprise, this new series is the long-awaited successor to the original Star Trek (1966). Under the command of Captain Jean-Luc Picard, the all new Enterprise NCC 1701-D travels out to distant planets to seek out new life and to boldly go where no one has gone before.","genre":["Mystery","Action","Adventure","Sci-Fi"],"director":null,"actors":[{"id":"035c4793-4864-45b8-8d4f-b86b454c60b0","name":"Marina Sirtis"},{"id":"5bddea2c-8609-499a-a444-77e0142743c0","name":"Jonathan Frakes"},{"id":"fc9f27d2-aaee-46e6-b263-40ec8d2dd355","name":"LeVar Burton"},{"id":"57a471b1-09dc-48fd-ba8a-1211015a0110","name":"Patrick Stewart"}],"writers":[{"id":"6960e2ca-889f-41f5-b728-1e7313e54d6c","name":"Gene Roddenberry"}]}',
            '{"id":"c9e1f6f0-4f1e-4a76-92ee-76c1942faa97","title":"Star Trek: Discovery","imdb_rating":7.3,"description":"Ten years before Kirk, Spock, and the Enterprise, the USS Discovery discovers new worlds and lifeforms as one Starfleet officer learns to understand all things alien.","genre":["Drama","Sci-Fi","Adventure","Action"],"director":null,"actors":[{"id":"3f123595-ecfb-4740-a1c5-ceab9fc21c23","name":"Anthony Rapp"},{"id":"861a3116-7f75-4b7c-b1a1-5efd4936589c","name":"Mary Wiseman"},{"id":"43bb73ff-0f0e-4169-b708-32a77dc1c50e","name":"Doug Jones"},{"id":"bd2a8ab8-a7bc-45cf-852b-d23cb1cf4b5d","name":"Sonequa Martin-Green"}],"writers":[{"id":"b670fa3e-9f7b-4786-a00c-09d95f1e7b5c","name":"Bryan Fuller"},{"id":"82b7dffe-6254-4598-b6ef-5be747193946","name":"Alex Kurtzman"}]}',
            '{"id":"a7b11817-205f-4e1a-98b5-e3c48b824bc3","title":"Star Trek","imdb_rating":6.4,"description":"A massive alien spacecraft of enormous power destroys three powerful Klingon cruisers, entering Federation space. Admiral James T. Kirk is ordered to take command of the USS Enterprise for the first time since her historic five-year mission. The Epsilon IX space station alerts the Federation, but they are also destroyed by the alien spacecraft. The only starship in range is the Enterprise--after undergoing a major overhaul at Spacedock on Earth. Kirk rounds up the rest of his crew, and acquires some new members, and sets off to intercept the alien spacecraft. However, it has been there years since Kirk last commanded the Enterprise... is he up to the task of saving Earth?","genre":["Mystery","Sci-Fi","Adventure"],"director":"Robert Wise","actors":[{"id":"5a3d0299-2df2-4070-9fda-65ff4dfa863c","name":"Leonard Nimoy"},{"id":"807ce9c3-6294-485c-803a-1975066f239f","name":"James Doohan"},{"id":"836bb95b-6db8-4418-a110-f41663b1c025","name":"DeForest Kelley"},{"id":"9758b894-57d7-465d-b657-c5803dd5b7f7","name":"William Shatner"}],"writers":[{"id":"317ba074-e7bf-4c7a-a6e3-da71b1e7cbf2","name":"Alan Dean Foster"},{"id":"6960e2ca-889f-41f5-b728-1e7313e54d6c","name":"Gene Roddenberry"},{"id":"207c28f1-2d25-4f6c-b3d2-1ba2a18c51de","name":"Harold Livingston"}]}',
        ]
    }

    assert data_json == expected
