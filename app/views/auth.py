from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel

from app.service.users import UserService
from app.dependencies import get_db, jwt_decode
from sqlalchemy.orm import Session

from app.dependencies import oauth2_scheme


# Models
class TokenRequest(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True


class RefreshTokensRequest(BaseModel):
    refresh_token: str


router = APIRouter(prefix='/auth', tags=['auth'])


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = UserService(db).get_all_by_filter({'username': username})[0]
    if not user:
        return False

    password_hash = user.get('password', None)

    if password_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No password set",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not UserService(db).check_password_with_hash(user_password=password, password_hash=password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def decoded_jwt(token: str = Depends(oauth2_scheme)):
    return jwt_decode(token)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=TokenResponse, summary='Получить токены')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Получить токены / Generate tokens
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    return UserService(db).gen_jwt({'username': user['username'], 'role': user['role']})


@router.put('', status_code=status.HTTP_201_CREATED, response_model=TokenResponse, summary='Обновить токены')
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
