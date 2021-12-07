from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Column, Integer, String
from app.dao.model.base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)  # to be deprecated for email
    password = Column(String)  # a hashed password
    role = Column(String)  # to be deprecated
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<User: id={self.id}, username={self.username}, role={self.role}>"


class UserBase(BaseModel):
    username: str
    password: Optional[str]
    role: str
    email: EmailStr
    name: str
    surname: str

    class Config:
        orm_mode = True


class UserBM(UserBase):
    id: Optional[int]


class UserUpdateBM(UserBase):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]
    email: Optional[EmailStr]
    name: Optional[str]
    surname: Optional[str]
