from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from app.dao.model.base import Base
from app.dao.model.genres import GenreBM


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    # username = Column(String, nullable=True)  # to be deprecated for email
    password = Column(String)  # a hashed password
    role = Column(String, default="user")  # to be deprecated
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String(100))  # , nullable=False)
    surname = Column(String(100))  # , nullable=False)
    favorite_genre = Column(Integer, ForeignKey('genre.id'))

    def __repr__(self):
        return f"<User: id={self.id}, email={self.username}, role={self.role}, name={self.name}" \
               f", surname={self.surname}>"


class UserBase(BaseModel):
    # username: Optional[str]
    password: Optional[str]
    role: Optional[str]
    email: EmailStr
    name: Optional[str]
    surname: Optional[str]
    favorite_genre: Optional[int]

    class Config:
        orm_mode = True


class UserBM(UserBase):
    id: Optional[int]
    # favorite_genre: Optional[GenreBM]


class UserInDB(UserBase):
    id: int


class UserUpdateBM(UserBase):
    # username: Optional[str]
    password: Optional[str]
    role: Optional[str]
    email: Optional[EmailStr]
    name: Optional[str]
    surname: Optional[str]
    favorite_genre: Optional[int]
