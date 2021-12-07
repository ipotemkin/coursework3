from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from app.dao.model.base import Base


class Director(Base):
    __tablename__ = 'director'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # surname = Column(String, default="...")
    # country = Column(String, default="...")
    # movies = db.relationship('Movie', lazy='dynamic')


class DirectorBM(BaseModel):
    id: Optional[int]
    name: str
    # surname: Optional[str]
    # country: Optional[str]

    class Config:
        orm_mode = True


class DirectorUpdateBM(BaseModel):
    name: str

    class Config:
        orm_mode = True
