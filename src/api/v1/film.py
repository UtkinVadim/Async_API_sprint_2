from http import HTTPStatus
from typing import List, Optional

from api.utils import add_filter_to_body, add_sort_to_body, generate_body
from fastapi import APIRouter, Depends, HTTPException, Query
from models.film_response import FilmDetailResponse, ShortFilmResponse
from services.film import FilmService, get_film_service
from strings.exceptions import FILM_NOT_FOUND

router = APIRouter()


@router.get("/search",
            response_model=List[ShortFilmResponse],
            summary="Поиск кинопроизведений",
            description="Полнотекстовый поиск по кинопроизведениям",
            response_description="Название и рейтинг фильма",
            tags=['полнотекстовый поиск', 'кино'],
            )
async def film_search(
        query: Optional[str] = Query(
            "", alias="query",
            title="запрос",
            description="Поисковый запрос",
        ),
        from_: Optional[str] = Query(
            None, alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        size: Optional[str] = Query(
            None, alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
        sort: Optional[str] = Query(
            None, regex="-?imdb_rating",
            title="сортировка",
            description="Сортировка результатов запроса по рейтингу",
        ),
        filter_genre_id: Optional[str] = Query(None, alias="filter[genre]",
                                               title="id жанра",
                                               description="id жанра для фильтрации",
                                               ),
        film_service: FilmService = Depends(get_film_service),
) -> Optional[List[ShortFilmResponse]]:
    """
    Поиск по фильмам с пагинацией, фильтрацией по жанрам и сортировкой

    :param query:
    :param from_:
    :param size:
    :param sort:
    :param filter_genre_id:
    :param film_service:
    :return:
    """
    if not query and query is not None:
        return

    body = await generate_body(query, from_, size)

    if sort:
        body = await add_sort_to_body(body, sort)

    if filter_genre_id:
        filter_genre = await film_service.get_genre_by_id(filter_genre_id)
        if not filter_genre:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
        body = await add_filter_to_body(body, filter_genre)

    result = await film_service.search(body=body)

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)

    return result


@router.get("/{film_id}",
            response_model=FilmDetailResponse,
            summary="Информация по конкретному кинопроизведению",
            description="Полная информация по одному конкретному кинопроизведению",
            response_description="Название, рейтинг, описание, жанр фильма и участники с разделением по ролям",
            tags=['подробный вывод', 'кино'],
            )
async def film_details(film_id: str = Query(...,
                                            title="id фильма",
                                            description="Id фильма по которому будет выведена полная информация",
                                            ),
                       film_service: FilmService = Depends(get_film_service)) -> FilmDetailResponse:
    """
    Отдаёт полную информацию по фильму
    GET /api/v1/film/<uuid:UUID>/

    :param film_id:
    :param film_service:
    :return:
    """
    film = await film_service.get_by_id(id_=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)

    return FilmDetailResponse(**film.dict())


@router.get("/", response_model=List[ShortFilmResponse],
            summary="Фильтр кинопроизведений",
            description="Фильтр по кинопроизведениям",
            response_description="Название и рейтинг фильма",
            tags=['фильтр', 'кино']
            )
async def film_filter(
        from_: Optional[str] = Query(
            None,
            alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        size: Optional[str] = Query(
            None,
            alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
        sort: Optional[str] = Query(
            None, regex="-?imdb_rating",
            title="сортировка",
            description="Сортировка результатов запроса по рейтингу",
        ),
        filter_genre_id: Optional[str] = Query(None, alias="filter[genre]",
                                               title="id жанра",
                                               description="id жанра для фильтрации",
                                               ),
        film_service: FilmService = Depends(get_film_service),
) -> List[ShortFilmResponse]:
    result = await film_search(
        query=None,
        from_=from_,
        size=size,
        sort=sort,
        filter_genre_id=filter_genre_id,
        film_service=film_service,
    )
    return result
