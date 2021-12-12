from app.dao.model.base import Base
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Column, Integer, String


class RToken(Base):
    __tablename__ = "r_token"
    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False, unique=True)


class RTokenBM(BaseModel):
    id: Optional[int]
    token: str

    class Config:
        orm_mode = True


class TokenRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


# a model for token response
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True


# a model to refresh tokens
class RefreshTokensRequest(BaseModel):
    access_token: str
    refresh_token: str


# a user model to make a token
class UserForTokenModel(BaseModel):
    email: EmailStr
    role: str

    class Config:
        orm_mode = True


# a full model for token
class TokenModel(UserForTokenModel):
    exp: int
