from fastapi import APIRouter, Depends
from app.service.movies import MovieService
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/movies', tags=['movies'])


@router.get('', summary='Получить все фильмы')
async def movies_get_all(director_id: int = None,
                         genre_id: int = None,
                         year: int = None,
                         page: int = None,
                         status: str = None,
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
        return MovieService(db).get_all_by_filter(query_d, page=page, state=status)

    return MovieService(db).get_all(page=page, state=status)


@router.get('/{pk}', summary='Получить фильм по ID')
async def movies_get_one(pk: int, db: Session = Depends(get_db)):
    """
    Получить фильм по ID:

    - **pk**: ID фильма
    """
    return MovieService(db).get_one(pk)
