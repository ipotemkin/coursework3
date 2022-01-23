from pydantic import BaseModel, EmailStr, Extra
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from app.dao.model.base import Base
import ujson


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    password = Column(String)  # a hashed password
    role = Column(String, default="user")  # to be deprecated
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String(100))  # , nullable=False)
    surname = Column(String(100))  # , nullable=False)
    favorite_genre = Column(Integer, ForeignKey("genre.id"))

    def __repr__(self):
        return (
            f"<User: id={self.id}, email={self.username}, role={self.role}, name={self.name}"
            f", surname={self.surname}>"
        )


class UserBase(BaseModel):
    password: Optional[str]
    role: Optional[str]
    email: EmailStr
    name: Optional[str]
    surname: Optional[str]
    favorite_genre: Optional[int]

    class Config:
        orm_mode = True
        json_loads = ujson.loads


class UserBM(UserBase):
    id: Optional[int]


class UserInDB(UserBase):
    id: int


class UserUpdateBM(BaseModel):
    # password: Optional[str]
    role: Optional[str]
    email: Optional[EmailStr]
    name: Optional[str]
    surname: Optional[str]
    favorite_genre: Optional[int]

    class Config:
        orm_mode = True
        json_loads = ujson.loads
        extra = Extra.forbid
