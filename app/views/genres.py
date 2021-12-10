from fastapi import APIRouter, Depends
from app.service.genres import GenreService
from app.dependencies import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix='/genres', tags=['genres'])


@router.get('', summary='Получить все жанры')
@router.get('/', summary='Получить все жанры', include_in_schema=False)
async def genres_get_all(page: int = None, db: Session = Depends(get_db)):
    """
    Получить все жанры
    """
    return GenreService(db).get_all(page=page)


@router.get('/{pk}', summary='Получить жанр по его ID')
async def genres_get_one(pk: int, db: Session = Depends(get_db)):
    """
    Получить жанр по ID:

    - **pk**: ID жанра
    """
    return GenreService(db).get_one(pk)
