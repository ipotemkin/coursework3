from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Response, Depends, Query, Path

from app.service.favorites import FavoriteMovieService
from app.dependencies import get_db, get_current_user

from typing import Optional

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/movies/", include_in_schema=False)
@router.get("/movies", summary="Получить любимые фильмы текущего пользователя")
async def favorites_get_all(
    page: Optional[int] = Query(
        None,
        title="Страница",
        description="Укажите номер страницы для постраничного вывода",
    ),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Получить любимые фильмы текущего пользователя
    """
    return FavoriteMovieService(db).get_all_by_user(user.get("id"), page=page)


@router.post(
    "/movies/{movie_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Добавить любимый фильм к текущему пользователю",
    response_description="The created item",
)
async def add_favorites_to_current_user(
    response: Response,
    movie_id: int = Path(..., title="ID фильма", description="Укажите ID фильма"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Добавить любимый фильм к текущему пользователю:

    - **movie_id**: ID фильма
    """
    new_obj = FavoriteMovieService(db).create(
        {"user_id": user.get("id"), "movie_id": movie_id}
    )
    response.headers["Location"] = f"{router.prefix}/{new_obj.id}"
    return new_obj


@router.delete(
    "/movies/{movie_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить любимый фильм у текущего пользователя",
)
async def del_favorites_of_current_user(
    movie_id: int = Path(..., title="ID фильма", description="Укажите ID фильма"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Удалить любимый фильм у текущего пользователя
    """
    favorite_id = (
        FavoriteMovieService(db)
        .get_all_by_filter({"user_id": user.get("id"), "movie_id": movie_id})[0]
        .get("id")
    )
    FavoriteMovieService(db).delete(favorite_id)
