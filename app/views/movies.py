from fastapi import APIRouter, status, Response, Depends
from app.dao.model.movies import MovieUpdateBM, MovieBMSimple
from app.service.movies import MovieService
from app.dependencies import get_db, valid_token, valid_admin_token
from sqlalchemy.orm import Session

router = APIRouter(prefix='/movies', tags=['movies'], dependencies=[Depends(valid_token)])


@router.get('', summary='Получить все фильмы')
async def movies_get_all(director_id: int = None,
                         genre_id: int = None,
                         year: int = None,
                         page: int = None,
                         db: Session = Depends(get_db)):
    """
    Получить все фильмы
    """
    query_d = {}
    if director_id:
        query_d['director_id'] = director_id
    if genre_id:
        query_d['genre_id'] = genre_id
    if year:
        query_d['year'] = year
    if query_d:
        return MovieService(db).get_all_by_filter(query_d, page=page)

    return MovieService(db).get_all(page=page)


@router.get('/{pk}', summary='Получить фильм по ID')
async def movies_get_one(pk: int, db: Session = Depends(get_db)):
    """
    Получить фильм по ID:

    - **pk**: ID фильма
    """
    return MovieService(db).get_one(pk)


@router.post('', status_code=status.HTTP_201_CREATED,
             summary='Добавить фильм',
             response_description="The created item",
             dependencies=[Depends(valid_admin_token)])
async def movies_post(movie: MovieBMSimple, response: Response, db: Session = Depends(get_db)):
    """
    Добавить фильм:

    - **id**: ID фильма - целое число (необязательный параметр)
    - **title**: название фильма (обязательный параметр)
    - **description**: описание фильма (обязательный параметр)
    - **rating**: рейтинг фильма
    - **director_id**: режиссер фильма (обязательный параметр)
    - **genre_id**: жанр фильма (обязательный параметр)
    - **year**: год выпуска фильма (обязательный параметр)
    - **trailer**: ссылка на трейлер (необязательный параметр)
    """
    new_obj = MovieService(db).create(movie.dict())
    response.headers['Location'] = f'{router.prefix}/{new_obj.id}'
    return []


@router.patch('/{pk}',
              # status_code=status.HTTP_204_NO_CONTENT,
              summary='Изменить запись о фильме с указанным ID',
              dependencies=[Depends(valid_admin_token)])
async def movies_update(movie: MovieUpdateBM, pk: int, db: Session = Depends(get_db)):
    """
    Изменить запись о фильме с указанным ID:

    - **title**: название фильма
    - **description**: описание фильма
    - **rating**: рейтинг фильма
    - **director_id**: режиссер фильма
    - **genre_id**: жанр фильма
    - **year**: год выпуска фильма
    - **trailer**: ссылка на трейлер
    """
    return MovieService(db).update(movie.dict(), pk)


@router.delete('/{pk}', status_code=status.HTTP_200_OK,
               summary='Удалить запись о фильме с указанным ID',
               dependencies=[Depends(valid_admin_token)])
async def movies_delete(pk: int, db: Session = Depends(get_db)):
    """
    Удалить запись о фильме с указанным ID:
    """
    MovieService(db).delete(pk)
