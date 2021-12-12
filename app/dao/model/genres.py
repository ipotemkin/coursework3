from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from app.dao.model.base import Base
import ujson


class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # movies = db.relationship('Movie', lazy='dynamic')


class GenreBM(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True
        json_loads = ujson.loads


class GenreUpdateBM(BaseModel):
    name: str

    class Config:
        orm_mode = True
        json_loads = ujson.loads
