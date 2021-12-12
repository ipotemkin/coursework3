from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from app.dao.model.base import Base
import ujson


class Director(Base):
    __tablename__ = "director"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # movies = db.relationship('Movie', lazy='dynamic')


class DirectorBM(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True
        json_loads = ujson.loads


class DirectorUpdateBM(BaseModel):
    name: str

    class Config:
        orm_mode = True
        json_loads = ujson.loads
