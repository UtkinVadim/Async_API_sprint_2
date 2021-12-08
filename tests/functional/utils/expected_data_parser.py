from typing import Union

from functional.utils.data_parser import DataParser


class ExpectedGenre:
    def __init__(self):
        self.parser = DataParser()
        self.file_data_path = "genres_data.json"

    async def get_expected_genres_data(self, genre_id: str = None) -> Union[list, dict, str]:
        genres_data_from_file = await self.parser.get_data_from_file(file_name=self.file_data_path)
        expected_data = [
            {"uuid": genres.get("id"), "name": genres.get("name")}
            for genres in map(lambda genre_data: genre_data.get("_source"), genres_data_from_file)
        ]
        if genre_id:
            for genre_expected_data in expected_data:
                if genre_id in genre_expected_data.values():
                    return genre_expected_data
            else:
                return f"В файле genres_data.json не найдена запись с id {genre_id}"
        return expected_data


class ExpectedPerson:
    def __init__(self):
        self.parser = DataParser()
        self.file_data_path = "persons_data.json"

    @staticmethod
    async def get_person_roles(film_ids: list) -> list:
        return [{film["id"]: film["role"]} for film in film_ids]

    async def get_expected_persons_data(self, person_id: str = None):
        persons_data_from_file = await self.parser.get_data_from_file(file_name=self.file_data_path)
        expected_data = [
            {
                "uuid": person.get("id"),
                "full_name": person.get("fullname"),
                "films": await self.get_person_roles(person.get("film_ids")),
            }
            for person in map(lambda person_data: person_data.get("_source"), persons_data_from_file)
        ]
        if person_id:
            for person_expected_data in expected_data:
                if person_id in person_expected_data.values():
                    return person_expected_data
            else:
                return f"В файле persons_data.json не найдена запись с id {person_id}"
        return expected_data

    async def get_expected_person_film_data(self, person_id: str):
        persons_data_from_file = await self.parser.get_data_from_file(file_name=self.file_data_path)
        person_data = list(filter(lambda person: person["_id"] == person_id, persons_data_from_file))[0]
        expected_data = [
            {"uuid": film_info.get("id"), "title": film_info.get("title"), "imdb_rating": film_info.get("imdb_rating")}
            for film_info in person_data["_source"]["film_ids"]
        ]
        return expected_data


class ExpectedFilm:
    def __init__(self):
        self.parser = DataParser()
        self.file_data_path = "films_data.json"

    async def get_film_detailed_data(self, film_id: str):
        films_data_from_file = await self.parser.get_data_from_file(file_name=self.file_data_path)
        film_data = list(filter(lambda film: film["_id"] == film_id, films_data_from_file))[0]["_source"]
        film_data.pop("actors_names")
        film_data.pop("writers_names")
        return film_data

    async def get_film_data(
        self, genre_id: str = None, page_size: int = None, page_number: int = None, sort_by: str = None
    ):
        films_data_from_file = await self.parser.get_data_from_file(file_name=self.file_data_path)
        films_data = [film_data["_source"] for film_data in films_data_from_file]
        if genre_id:
            genre_parser = ExpectedGenre()
            genre = await genre_parser.get_expected_genres_data(genre_id)
            films_data = list(
                filter(lambda film_data: film_data if genre["name"] in film_data["genre"] else None, films_data)
            )

        films_data = [
            {"id": film["id"], "title": film["title"], "imdb_rating": film["imdb_rating"]} for film in films_data
        ]

        if sort_by:
            reverse = False
            if "-" in sort_by:
                sort_by = sort_by[1:]
                reverse = True
            films_data = sorted(films_data, key=lambda film: film[sort_by], reverse=reverse)
        if page_number and page_size:
            films_data = films_data[(page_number - 1) * page_size : page_number * page_size]
        elif page_size:
            films_data = films_data[:page_size]
        return films_data
