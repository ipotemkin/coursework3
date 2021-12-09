from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Response, Depends

from app.dao.model.favotites import FavoriteMovieBM
from app.dao.model.users import UserInDB

from app.service.favorites import FavoriteMovieService

from app.dependencies import get_db, get_current_user

router = APIRouter(prefix='/favorites', tags=['favorites'])


@router.get('/movies/', include_in_schema=False)
@router.get('/movies', summary='Получить любимые фильмы текущего пользователя')
async def favorites_get_all(
        page: int = None,
        db: Session = Depends(get_db),
        user: UserInDB.dict = Depends(get_current_user)):
    """
    Получить любимые фильмы текущего пользователя
    """
    return FavoriteMovieService(db).get_all_by_user(user.get('id'), page=page)


@router.post('', status_code=status.HTTP_201_CREATED, summary='Добавить запись юзер–любимый фильм',
             response_description="The created item")
async def favorites_post(record: FavoriteMovieBM, response: Response, db: Session = Depends(get_db)):
    """
    Добавить запись юзер–любимый фильм:

    - **id**: ID жанра - целое число (необязательный параметр)
    - **user_id**: ID пользователя (обязательный параметр)
    - **movie_id**: ID фильма (обязательный параметр)
    """
    new_obj = FavoriteMovieService(db).create(record.dict())
    response.headers['Location'] = f'{router.prefix}/{new_obj.id}'
    return new_obj


@router.post(
    '/movies/{movie_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Добавить любимый фильм к текущему пользователю',
    response_description="The created item",
    # dependencies=[Depends(valid_token())]
    )
async def add_favorites_to_current_user(
        movie_id: int,
        response: Response,
        db: Session = Depends(get_db),
        user: UserInDB.dict = Depends(get_current_user)
        ):
    """
    Добавить любимый фильм к текущему пользователю:

    - **id**: ID жанра - целое число (необязательный параметр)
    - **movie_id**: ID фильма (обязательный параметр)
    """
    new_obj = FavoriteMovieService(db).create({'user_id': user.get('id'), 'movie_id': movie_id})
    response.headers['Location'] = f'{router.prefix}/{new_obj.id}'
    return new_obj


@router.delete(
    '/movies/{movie_id}',
    status_code=status.HTTP_200_OK,
    summary='Удалить запись о жанре с указанным ID')
async def del_favorites_of_current_user(
        movie_id: int,
        db: Session = Depends(get_db),
        user: UserInDB.dict = Depends(get_current_user),
        ):
    """
    Удалить запись о жанре с указанным ID:
    """
    favorite_id = FavoriteMovieService(db).get_all_by_filter(
        {'user_id': user.get('id'), 'movie_id': movie_id})[0].get('id')
    FavoriteMovieService(db).delete(favorite_id)
