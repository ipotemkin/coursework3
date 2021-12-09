from fastapi import APIRouter, status, Response, Depends
from app.dao.model.favotites import FavoriteMovieBM
from app.service.favorites import FavoriteMovieService
from app.service.users import UserService
from app.dependencies import get_db, valid_token
from sqlalchemy.orm import Session


router = APIRouter(prefix='/favorites', tags=['favorites'])


@router.get('/movies/', include_in_schema=False)
@router.get('/movies', summary='Получить любимые фильмы текущего пользователя')
async def favorites_get_all(page: int = None,
                            db: Session = Depends(get_db),
                            decoded_token=Depends(valid_token)):
    """
    Получить любимые фильмы текущего пользователя
    """
    user_id = UserService(db).get_all_by_filter({'email': decoded_token.get('email')})[0].get('id')
    return FavoriteMovieService(db).get_all_by_user(user_id)
    # return FavoriteMovieService(db).get_all(page=page)


# @router.get('/movies/{pk}', summary='Получить жанр по его ID')
# async def genres_get_one(pk: int, db: Session = Depends(get_db)):
#     """
#     Получить жанр по ID:
#
#     - **pk**: ID жанра
#     """
#     return GenreService(db).get_one(pk)
#

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


# @router.post('', status_code=status.HTTP_201_CREATED, summary='Добавить запись юзер–любимый фильм',
#              response_description="The created item")
# async def favorites_post(record: FavoriteMovieBM, response: Response, db: Session = Depends(get_db)):
#     """
#     Добавить запись юзер–любимый фильм:
#
#     - **id**: ID жанра - целое число (необязательный параметр)
#     - **user_id**: ID пользователя (обязательный параметр)
#     - **movie_id**: ID фильма (обязательный параметр)
#     """
#     new_obj = FavoriteMovieService(db).create(record.dict())
#     response.headers['Location'] = f'{router.prefix}/{new_obj.id}'
#     return new_obj

@router.post('/movies/{movie_id}', status_code=status.HTTP_201_CREATED,
             summary='Добавить любимый фильм к текущему пользователю',
             response_description="The created item",
             # dependencies=[Depends(valid_token())]
             )
async def favorites_post(movie_id: int,
                         response: Response,
                         db: Session = Depends(get_db),
                         decoded_token=Depends(valid_token)):
    """
    Добавить любимый фильм к текущему пользователю:

    - **id**: ID жанра - целое число (необязательный параметр)
    - **movie_id**: ID фильма (обязательный параметр)
    """
    user_id = UserService(db).get_all_by_filter({'email': decoded_token.get('email')})[0].get('id')
    new_obj = FavoriteMovieService(db).create({'user_id': user_id, 'movie_id': movie_id})
    response.headers['Location'] = f'{router.prefix}/{new_obj.id}'
    return new_obj


@router.delete('/movies/{movie_id}', status_code=status.HTTP_200_OK,
               summary='Удалить запись о жанре с указанным ID')
async def genres_delete(movie_id: int,
                        db: Session = Depends(get_db),
                        decoded_token=Depends(valid_token)
                        ):
    """
    Удалить запись о жанре с указанным ID:
    """
    user_id = UserService(db).get_all_by_filter({'email': decoded_token.get('email')})[0].get('id')
    favorite_id = FavoriteMovieService(db).get_all_by_filter({'user_id': user_id, 'movie_id': movie_id})[0].get('id')
    FavoriteMovieService(db).delete(favorite_id)
    # return None



# @router.patch('/{pk}',
#               # status_code=status.HTTP_204_NO_CONTENT,
#               summary='Изменить запись о жанре с указанным ID')
# async def genres_update(genre: GenreUpdateBM, pk: int, db: Session = Depends(get_db)):
#     """
#     Изменить запись о жанре с указанным ID:
#
#     - **name**: изменить название жанра
#     """
#     return GenreService(db).update(genre.dict(), pk)


# @router.delete('/{pk}', status_code=status.HTTP_200_OK, summary='Удалить запись о жанре с указанным ID')
# async def genres_delete(pk: int, db: Session = Depends(get_db)):
#     """
#     Удалить запись о жанре с указанным ID:
#     """
#     GenreService(db).delete(pk)
#     # return None
