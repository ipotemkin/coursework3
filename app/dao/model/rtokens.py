from app.dao.model.base import Base
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Column, Integer, String


class RToken(Base):
    __tablename__ = 'r_token'
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


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True


class RefreshTokensRequest(BaseModel):
    access_token: str
    refresh_token: str
