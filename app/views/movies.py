from fastapi import APIRouter, Depends, Query, Path
from app.service.movies import MovieService
from app.dependencies import get_db, Page
from sqlalchemy.orm import Session
from typing import Optional
from enum import Enum

router = APIRouter(prefix="/movies", tags=["movies"])


class IsNew(str, Enum):
    new = "new"


@router.get("", summary="Получить все фильмы")
@router.get("/", include_in_schema=False)
async def movies_get_all(
    director_id: Optional[int] = Query(
        None, title="ID режиссера", description="Укажите ID режиссера"
    ),
    genre_id: Optional[int] = Query(
        None, title="ID жанра", description="Укажите ID жанра"
    ),
    year: Optional[int] = Query(
        None, title="Год выпуска", description="Укажите год выпуска фильма"
    ),
    page=Depends(Page),
    status: Optional[IsNew] = Query(
        None,
        title="Статус",
        description="Укажите new, чтобы вывести сначала новые фильмы",
    ),
    db: Session = Depends(get_db),
):
    """
    Получить все фильмы. Можно в качестве фильтра, задать ID режиссера, ID жанра, год выпуска
    """
    query_d = {}
    if director_id:
        query_d["director_id"] = director_id
    if genre_id:
        query_d["genre_id"] = genre_id
    if year:
        query_d["year"] = year
    if query_d:
        return MovieService(db).get_all_by_filter(
            query_d, page=page.value, state=status
        )

    return MovieService(db).get_all(page=page.value, state=status)


@router.get("/{pk}", summary="Получить фильм по ID")
async def movies_get_one(
    pk: int = Path(..., title="ID фильма", description="Укажите ID фильма"),
    db: Session = Depends(get_db),
):
    """
    Получить фильм по ID:

    - **pk**: ID фильма
    """
    return MovieService(db).get_one(pk)
