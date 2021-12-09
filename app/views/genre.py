from fastapi import APIRouter, status, Response, Depends
from sqlalchemy.orm import Session

from app.dao.model.genres import GenreBM, GenreUpdateBM
from app.service.genres import GenreService
from app.dependencies import get_db, valid_token
from app.service.users import UserService


router = APIRouter(prefix='/genre', tags=['genres'])


@router.get('', summary='Получить жанр текущего пользователя')
@router.get('/', include_in_schema=False)
async def genre_get_one_of_current_user(db: Session = Depends(get_db),
                                        decoded_token=Depends(valid_token)
                                        ):
    """
    Получить жанр текущего пользователя
    """
    genre_id = UserService(db).get_all_by_filter({'email': decoded_token.get('email')})[0].get('favorite_genre')
    return GenreService(db).get_one(genre_id)['name']


# @router.get('/{pk}', summary='Получить жанр по его ID')
# async def genres_get_one(pk: int, db: Session = Depends(get_db)):
#     """
#     Получить жанр по ID:
#
#     - **pk**: ID жанра
#     """
#     return GenreService(db).get_one(pk)
#
#
# @router.post('', status_code=status.HTTP_201_CREATED, summary='Добавить жанр',
#              response_description="The created item")
# async def genres_post(genre: GenreBM, response: Response, db: Session = Depends(get_db)):
#     """
#     Добавить жанр:
#
#     - **id**: ID жанра - целое число (необязательный параметр)
#     - **name**: название жанра (обязательный параметр)
#     """
#     new_obj = GenreService(db).create(genre.dict())
#     response.headers['Location'] = f'{router.prefix}/{new_obj.id}'
#     return []
#
#
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
#
#
# @router.delete('/{pk}', status_code=status.HTTP_200_OK, summary='Удалить запись о жанре с указанным ID')
# async def genres_delete(pk: int, db: Session = Depends(get_db)):
#     """
#     Удалить запись о жанре с указанным ID:
#     """
#     GenreService(db).delete(pk)
#     # return None
