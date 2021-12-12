from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.service.genres import GenreService
from app.dependencies import get_db, valid_token
from app.service.users import UserService
from app.dao.model.rtokens import TokenModel


router = APIRouter(prefix='/genre', tags=['genres'])


@router.get('', summary='Получить жанр текущего пользователя')
@router.get('/', include_in_schema=False)
async def genre_get_one_of_current_user(db: Session = Depends(get_db),
                                        decoded_token: TokenModel = Depends(valid_token)
                                        ):
    """
    Получить жанр текущего пользователя
    """
    genre_id = UserService(db).get_all_by_filter({'email': decoded_token.email})[0].get('favorite_genre')
    return GenreService(db).get_one(genre_id)['name']
