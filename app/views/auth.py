from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.service.users import UserService
from app.dependencies import get_db
from sqlalchemy.orm import Session

from app.dao.model.users import UserBM
from app.dao.model.rtokens import TokenRequest, TokenResponse, RefreshTokensRequest


router = APIRouter(prefix="/auth", tags=["auth"])


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user = UserService(db).get_all_by_filter({"email": email})[0]
    if not user:
        return False

    password_hash = user.get("password", None)

    if password_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No password set",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not UserService(db).check_password_with_hash(
        user_password=password, password_hash=password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# authentication via Swagger using OAuth2 form
@router.post(
    "/login_oauth2",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
    summary="Получить токены",
)
async def login_oauth2(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Получить токены / Generate tokens
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    return UserService(db).gen_jwt({"email": user["email"], "role": user["role"]})


@router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
    summary="Получить токены",
)
async def login_for_access_token(
    login_user: TokenRequest, db: Session = Depends(get_db)
):
    """
    Получить токены / Generate tokens
    """
    user = authenticate_user(login_user.email, login_user.password, db)
    return UserService(db).gen_jwt({"email": user["email"], "role": user["role"]})


@router.put(
    "/login",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
    summary="Обновить токены",
)
async def refresh_tokens(body: RefreshTokensRequest, db: Session = Depends(get_db)):
    """
    Обновить токены / Refresh tokens
    """
    if not UserService(db).check_refresh_token(body.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token non valid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserService(db).refresh_jwt(body.refresh_token)


# TODO Remove this endpoint
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Добавить пользователя",
    response_description="The created item",
)
async def users_post(user: UserBM, response: Response, db: Session = Depends(get_db)):
    """
    Добавить пользователя:

    - **id**: ID пользователя - целое число (необязательный параметр)
    - **email**: email пользователя - используется для его идентификации (обязательный параметр)
    - **password**: пароль пользователя
    - **name**: имя пользователя
    - **surname**: фамилия пользователя
    - **role**: роль пользователя ('user' или 'admin')
    - **favorite_genre**: ссылка на любимый жанр (=ID жанра)
    """
    new_obj = UserService(db).create(user.dict())
    response.headers["Location"] = f"{router.prefix}/{new_obj.id}"
    # return new_obj
    return UserBM.from_orm(new_obj).dict(exclude={'password'})
