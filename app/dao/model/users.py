from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from app.dao.model.base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String)
    role = Column(String)

    def __repr__(self):
        return f"<User: id={self.id}, username={self.username}, role={self.role}>"


class UserBase(BaseModel):
    username: str
    password: Optional[str]
    role: str

    class Config:
        orm_mode = True


class UserBM(UserBase):
    id: Optional[int]


class UserUpdateBM(UserBase):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]
