from fastapi import APIRouter, Depends, Query, Path
from app.service.genres import GenreService
from app.dependencies import get_db
from sqlalchemy.orm import Session
from typing import Optional


router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("", summary="Получить все жанры")
@router.get("/", summary="Получить все жанры", include_in_schema=False)
async def genres_get_all(
    page: Optional[int] = Query(
        None,
        title="Страница",
        description="Укажите номер страницы для постраничного вывода",
    ),
    db: Session = Depends(get_db),
):
    """
    Получить все жанры
    """
    return GenreService(db).get_all(page=page)


@router.get("/{pk}", summary="Получить жанр по его ID")
async def genres_get_one(
    pk: int = Path(..., title="ID жанра", description="Укажите ID жанра"),
    db: Session = Depends(get_db),
):
    """
    Получить жанр по ID:

    - **pk**: ID жанра
    """
    return GenreService(db).get_one(pk)
