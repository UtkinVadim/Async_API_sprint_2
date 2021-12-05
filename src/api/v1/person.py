from http import HTTPStatus
from typing import List, Optional

from api.v1.film import generate_body
from fastapi import APIRouter, Depends, HTTPException, Query
from models.person_response import PersonFilmResponse, PersonResponse
from services.person import PersonService, get_person_service
from strings.exceptions import PERSON_NOT_FOUND

router = APIRouter()


@router.get("/search", response_model=List[PersonResponse],
            summary="Поиск по персоналиям в кино",
            description="Полнотекстовый поиск по персоналиям, участвовавшим в создании кино",
            response_description="id и имя человека, а также список фильмов в которых он участвовал",
            tags=['полнотекстовый поиск', 'персоналии'],
            )
async def person_search(
        query: Optional[str] = Query(
            "",
            title="запрос",
            description="Поисковый запрос",
        ),
        page_number: Optional[str] = Query(
            None, alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        page_size: Optional[str] = Query(
            None, alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
        service: PersonService = Depends(get_person_service),
) -> List[PersonResponse]:
    body = await generate_body(query, page_number, page_size)
    searched_persons = await service.search(body=body)
    if not searched_persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return [
        PersonResponse(uuid=person.id, full_name=person.fullname,
                       films=[{film.id: film.role} for film in person.film_ids])
        for person in searched_persons
    ]


@router.get("/{person_id}", response_model=PersonResponse,
            summary="Информация по конкретному человеку",
            description="Полная информация по одному конкретному человеку",
            response_description="id и имя человека, а также список фильмов в которых он участвовал",
            tags=['подробный вывод', 'персоналии'],
            )
async def person_details(person_id: str = Query(...,
                                                title="id персоны",
                                                description="Id персоны по которому будет выведена полная информация",
                                                ),
                         person_service: PersonService = Depends(get_person_service)) -> PersonResponse:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return PersonResponse(uuid=person.id, full_name=person.fullname,
                          films=[{film.id: film.role} for film in person.film_ids])


@router.get("/{person_id}/film", response_model=List[PersonFilmResponse])
async def person_films(person_id: str, person_service: PersonService = Depends(get_person_service)) -> List[
    PersonFilmResponse]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)

    return [PersonFilmResponse(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in
            person.film_ids]
