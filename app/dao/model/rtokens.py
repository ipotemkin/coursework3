from app.dao.model.base import Base
from pydantic import BaseModel
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
